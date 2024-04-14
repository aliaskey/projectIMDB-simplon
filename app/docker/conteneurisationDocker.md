docker build . -t projetimdb

docker run -it -p 8501:8501/tcp projetimdb: latest


dockerfile :
FROM python:3

WORKDIR /Project_IMBD

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

    COPY requirements.txt .


RUN git clone https://github.com/AntoanetaStoyanova/PROJECT-IMBD.git 

RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/IMDB

ENTRYPOINT ["streamlit", "run", "code_API_Streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"] 
