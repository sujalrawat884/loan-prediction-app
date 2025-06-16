# Base Image
FROM python:3.9

# Working Directory
WORKDIR /app

#copy
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit","run","app.py"]


