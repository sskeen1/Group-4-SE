FROM python:3
RUN python -m pip install --upgrade pip
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY scamazon/requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./scamazon /code/
CMD sh init.sh && python3 scamazon/manage.py runserver 0.0.0.0:8000