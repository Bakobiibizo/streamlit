# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN python -m pip install pip --upgrade
RUN pip install wheel setuptools -q
RUN pip install python-dotenv -q
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN echo export PATH=~/.local/bin:/usr/bin:/bin:$PATH >> ~/.bashrc
RUN exec $SHELL
RUN pip install -r requirements.txt


EXPOSE 9090

HEALTHCHECK CMD curl --fail http://localhost:9090/_stcore/health

ENTRYPOINT ["/bin/bash",]