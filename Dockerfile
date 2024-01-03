# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /milan/services/speer_notes

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./gist_extension.sh .
RUN ./gist_extension.sh

RUN apt-get update && apt-get install -y netcat

# copy project
COPY . /milan/services/speer_notes

# run entrypoint.sh
ENTRYPOINT ["/milan/services/speer_notes/entrypoint.sh"]