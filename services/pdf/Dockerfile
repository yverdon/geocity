FROM python:3.10-slim-bullseye

# weasyprint deps as per https://doc.courtbouillon.org/weasyprint/stable/first_steps.html
RUN apt-get update && apt-get install -y libpango-1.0-0 libpangoft2-1.0-0

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

ADD app.py app.py

RUN mkdir /io

ENTRYPOINT ["python3" , "app.py"]
