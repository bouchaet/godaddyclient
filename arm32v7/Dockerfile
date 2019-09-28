FROM resin/raspberrypi3-python:3.6

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "./gdapiclient.py"]