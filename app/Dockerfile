FROM python:3

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y python3

COPY . /app

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "code_API_Streamlit.py"]


