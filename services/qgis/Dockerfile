FROM qgis/qgis:release-3_24

# ADD requirements.txt requirements.txt
# RUN pip install -r requirements.txt

ENV QT_QPA_PLATFORM=offscreen

WORKDIR /app

ADD app.py app.py

ENTRYPOINT ["python3" , "app.py"]
