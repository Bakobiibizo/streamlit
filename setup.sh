#! /bin/bash

curl -sSL https://install.python-poetry.org | python3 -

export PATH="$HOME/.poetry/bin:$PATH"
source $HOME/.poetry/env

sudo apt install -y python3-venv
sudo apt install -y python3-dev
sudo apt install -y python3-pip
sudo apt install -y libssl-dev
sudo apt install -y libffi-dev
sudo apt install -y build-essential
sudo apt install -y python-is-python3
sudo apt install -y ffmpeg
sudo apt install -y git
sudo apt install -y curl
sudo apt install -y wget
sudo apt install -y unzip
sudo apt install -y git-lfs

python -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip

poetry init 
poetry add streamlit
poetry add langchain
poetry add openai
poetry add tiktoken
poetry add chromadb
poetry add python-dotenv

poetry install

poetry shell

pip freeze > requirements.txt





