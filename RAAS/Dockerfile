FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements-tux.txt requirements-tux.txt
COPY lemmatization-fr.txt . 
RUN pip3 install -r requirements-tux.txt
RUN python -m spacy download fr_core_news_sm
COPY ratio.py .
COPY bot_discord.py .
CMD [ "python", "bot_discord.py" ]
