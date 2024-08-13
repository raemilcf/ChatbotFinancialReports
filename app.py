
import os
import pandas as pd 
import numpy as np
from werkzeug.utils import secure_filename
import torch
from transformers import BertTokenizer, BertForQuestionAnswering
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from utils import utils_finance
from flask import Flask, g, render_template, request,jsonify



Gfinancial_df = pd.DataFrame()
GtablesList = [] 
Gdocument_embeddings= []
Gchunks_text=  []

# Initialize the tokenizer and model
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForQuestionAnswering.from_pretrained(model_name)

model_Questions = pipeline("question-answering", model=model, tokenizer=tokenizer)

#initialize embedings 
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def load_global_data(pathFile):
    if 'financial_df' not in g or 'tablesList' not in g or 'document_embeddings' not in g or 'chunks_text' not in g:
        print('load data financial')
        g.financial_df, g.tablesList, g.document_embeddings, g.chunks_text = getData(pathFile)
    return g.financial_df, g.tablesList, g.document_embeddings, g.chunks_text



def getData(filePath):
    if filePath == '' :
        financial_df = pd.read_csv('static/data/finnacial_release_df.csv')
        table0 = pd.read_csv('static/data/table_0.csv')
        table1 = pd.read_csv('static/data/table_1.csv')
        table2 = pd.read_csv('static/data/table_2.csv')
        table3 = pd.read_csv('static/data/table_3.csv')
        table4 = pd.read_csv('static/data/table_4.csv')
        table5 = pd.read_csv('static/data/table_5.csv')
        table6 = pd.read_csv('static/data/table_6.csv')
        table7 = pd.read_csv('static/data/table_7.csv')
        table8 = pd.read_csv('static/data/table_8.csv')
        table9 = pd.read_csv('static/data/table_9.csv')

        tablesList = [table0, table1, table2, table3, table4, table5, table6, table7, table8, table9]


        # Apply the sentence tokenizer to each row in the DataFrame
        financial_df['sentences'] = financial_df['extracted_text'].apply(utils_finance.split_text_to_sentences)

        # Create one list of all sentences
        #all_sentences = [sentence for sublist in financial_df['sentences'] for sentence in sublist]

        #chuncks of text, extracted from pdf
        chunks_text = [sublist for sublist in financial_df['extracted_text'] ]

        # Create embeddings for documents
        document_embeddings = embedder.encode(chunks_text, convert_to_tensor=False)


    return financial_df, tablesList, document_embeddings, chunks_text




# cosine similarity of the embedings and return the best options 
def retrieve_context(question, document_embeddings, documents, top_k=1):
    question_embedding = embedder.encode(question, convert_to_tensor=False)
    
    document_embeddings = torch.tensor(document_embeddings)
    
    # using pytorch calculate cosine similarity
    scores = util.pytorch_cos_sim(question_embedding, document_embeddings)[0]
    
    # Move scores back to CPU and convert to numpy array
    scores = scores.cpu().numpy()
    
    # Retrieve the top_k results
    top_results = np.argpartition(-scores, range(top_k))[0:top_k]
    
    return [documents[idx] for idx in top_results]

#get response from model, after embeding text and extractign contexxt 
def get_response(question):
    financial_df, tablesList, document_embeddings, chunks_text = load_global_data('')

    # Retrieve relevant context base on the consine similarity
    context = retrieve_context(question, document_embeddings, chunks_text)
    

    # Answer the question using BertForQuestionAnswering
    result = model_Questions(question=question, context=" ".join(context))

    #check data on tables 
    relevant_Tables= utils_finance.check_allTables_relevan_data(question, tablesList)


    return result['answer'] , relevant_Tables







app = Flask(__name__)
app.static_folder = 'static'

#config folder to read data
app.config['UPLOAD_FOLDER'] = 'static/data'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["GET"])
def get_bot_response():
    userText = request.args.get('msg')

    result, relevant_Tables = get_response(userText)
    print(result)

   
    return  jsonify({
        'result': result,
        'relevant_Tables': relevant_Tables
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    message = request.form.get('message')
    file = request.files.get('file')

    #load new file 
    # load_global_data()

    
    if file:
        # Process the file here (e.g., save it, read it, etc.)
        filename = secure_filename(file.filename)
        file.save(os.path.join('pdfFiles', filename))
        return jsonify({'response': f'File {filename} uploaded successfully!'})
    
    # Process the text message
    #response = process_user_message(message)
    return "file uploaded!" #jsonify({'response': response})



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4900)
    app.run()