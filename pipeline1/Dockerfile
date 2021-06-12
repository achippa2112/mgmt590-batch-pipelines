FROM python

FROM tensorflow/tensorflow

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY gcs.py /app/gcs.py
