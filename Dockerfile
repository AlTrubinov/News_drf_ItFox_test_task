FROM python:3.10.4

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/news_drf

RUN apt-get update \
    && apt-get install netcat -y
RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/requirements.txt
RUN pip install --no-cache-dir -r /usr/src/requirements.txt

COPY . /usr/src/news_drf

ENTRYPOINT ["/usr/src/news_drf/entrypoint.sh"]







#FROM python:3.10.4
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONBUFFERED 1
#
#WORKDIR /usr/src/news_drf
#
#COPY ./requirements.txt /usr/src/requirements.txt
#RUN pip install --no-cache-dir -r /usr/src/requirements.txt
#
#COPY . /usr/src/news_drf
#
#EXPOSE 8000
