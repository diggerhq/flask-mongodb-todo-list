FROM python:3.11-slim-buster

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

COPY . /app

WORKDIR /app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]