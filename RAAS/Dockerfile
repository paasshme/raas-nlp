FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements-tux.txt requirements-tux.txt
COPY lemmatization-fr.txt . 
RUN pip3 install -r requirements-tux.txt
RUN python -m spacy download fr_core_news_sm
COPY ./assets ./assets
COPY ratio.py .
COPY bot_discord.py .
ENV FR_MODEL=fr_core_news_sm
ENV LEMMA_FILE=lemmatization-fr.txt

CMD [ "python", "bot_discord.py" ]
