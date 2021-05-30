# FROM rasa/rasa:latest-full 
FROM python:3.8.0-slim

WORKDIR /app
COPY . /app
COPY ./data /app/data
COPY ./domain /app/domain
COPY ./context /app/context

# Install git
RUN apt-get update && apt-get install -y git

# Install production dependencies.
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Download spacy requirements
RUN python -m spacy download en_core_web_md
RUN python -m spacy link en_core_web_md en

RUN python -m rasa train --domain=domain

VOLUME /app
VOLUME /app/data
VOLUME /app/models
VOLUME /app/channels
VOLUME /app/services

# ENTRYPOINT [ "/bin/bash" ]
# CMD ["-c", "rasa run -m /app/models --enable-api --cors * --debug -p ${PORT}"]
CMD ["python","-m","rasa","run","-m","/app/models","--enable-api","--cors","*","--debug", "-p", "8080" ]