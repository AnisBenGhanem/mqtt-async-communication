FROM python

COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

COPY subscriber.py subscriber.py

CMD ["python3","-u","subscriber.py"]