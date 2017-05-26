FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /lebaguette
WORKDIR /lebaguette
ADD requirements.txt /lebaguette/
RUN pip install -r requirements.txt
