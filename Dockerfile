FROM python:3.6-jessie

ENV DEBUG_MODE=False
ENV ACCESS_LOG_MODE=False

COPY walker /walker

WORKDIR walker

RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"

RUN apt-get update && apt-get install -y docker-ce

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

ENTRYPOINT ["python", "run.py"]
