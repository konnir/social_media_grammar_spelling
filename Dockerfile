FROM python:3.11-slim-buster
LABEL authors="nirkon"

#RUN apk add --no-cache build-base libffi-dev

WORKDIR /app
COPY model/. /app/model
COPY tweet_predict/. /app/tweet_predict
COPY demo_texts/. /app/demo_texts
COPY static/. /app/static
COPY templates/. /app/templates
COPY tweets_server.py /app
COPY requirements_docker.txt /app

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements_docker.txt && \
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    rm -rf /root/.cache/pip/*

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 8082

CMD ["uvicorn", "tweets_server:app", "--host", "0.0.0.0", "--port", "8082"]