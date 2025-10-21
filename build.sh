#!/usr/bin/env bash
set -o errexit

# Install MeCab and dictionary
apt-get update -o Acquire::AllowInsecureRepositories=true || true
apt-get install -y mecab libmecab-dev mecab-ipadic-utf8

# Then install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
