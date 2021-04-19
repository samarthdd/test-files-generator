FROM      python:3.9.3-alpine3.12

RUN       apk update && apk upgrade && \
          apk add --no-cache bash git openssh  build-base jpeg-dev zlib-dev libxslt-dev

WORKDIR   /app

COPY      . .
RUN       pip install -r requirements.txt
ENV       PYTHONPATH=.
CMD       python api/Server.py
EXPOSE    8881