# syntax=docker/dockerfile:1

FROM python:3.12

WORKDIR /chatbotfinancial

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
#run docker cmd to create app in docker 
# docker build -t app .
#run app in specified port 
# docker run -d -p 4900:4900 
#docker ps    # Find the container  ID
# docker stop <container_id>