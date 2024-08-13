import pandas as pd 
from fuzzywuzzy import fuzz
from prettytable import PrettyTable
import nltk
from nltk.tokenize import sent_tokenize
from flask import render_template_string

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt_tab')

def get_relevant_data(question, table_df):
    try:
        # Normalize the query
        question = question.lower().strip()

        # Use fuzzy matching for more flexible querying
        def match_row(row):
            row_str = row.astype(str).str.lower().str.strip()
            for cell in row_str:
                if fuzz.partial_ratio(question, cell) > 80:  # Threshold can be adjusted
                    return True
            return False

        matched_rows = table_df.apply(match_row, axis=1)
        results = table_df[matched_rows]

        if not results.empty:
            if len(results) > 10:
                results = results.head(10)
            return results
        else:
            return pd.DataFrame()  # Return an empty DataFrame if no results are found
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return pd.DataFrame()  # Retur
    

def dataframe_to_prettytable(df):
    """Convert DataFrame to PrettyTable."""
    if df.empty:
        return None

    table = PrettyTable()
    table.field_names = df.columns.tolist()

    for index, row in df.iterrows():
        table.add_row(row.tolist())

    return table


def check_allTables_relevan_data(question, tablesList):

    # Use a simple template to render the HTML table
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Data Table</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <style>
                .table-small {
                    font-size: 0.75em; /* Adjust the font size as needed */
                }
                 .table-container {
                    width: 75%; /* 75% of 750px = 562.5px */
                    overflow-x: auto; /* Enable horizontal scrolling if the content overflows */
                    margin-bottom: 20px;
                }
                .table-container table {
                    width: 100%; /* Make the table fit within the container */
                    font-size: 0.75em; /* Adjust font size */
                }
        </style>
    </head>
    <body>
        <div class="container">
            <p style='font-size:14px'>Financial Data</p>
            {{ tables | safe }}
        </div>
    </body>
    </html>
    """

    # Process each table and convert to HTML
    table_html_list = []
    for i, table in enumerate(tablesList, start=1):
        # Replace this with the actual function to get relevant data
        data = get_relevant_data(question, table)
        
        if not data.empty:
            html_table = data.to_html(classes='table table-striped table-small', index=False)
            table_html_list.append(f"<p style='font-size:12px'>Relevant data from Table {i}:</h4>{html_table}")
        # else:
        #     return ''

    # Join all HTML content
    combined_html = "<br>".join(table_html_list)
    
    # Render the final HTML template with all table data
    return render_template_string(template, tables=combined_html)

#convert document to sentences 
def split_text_to_sentences(text):
    return sent_tokenize(text)