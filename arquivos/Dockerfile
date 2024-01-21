FROM python:3.11.4
EXPOSE 5000
WORKDIR /arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#CMD ["gunicorn","--bind","0.0.0.0:80","app:create_app()"]  #para rodar o gunicorn
#para rodar localmente use o cmd abaixo, senao comente ele
CMD ["flask","run","--host","0.0.0.0"]  