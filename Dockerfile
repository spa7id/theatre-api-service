FROM python:3.9-slim
LABEL maintainer="spa7id"

ENV PYTHONUNBUFFERED 1
WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


RUN pip install -r requirements.txt

COPY . .
COPY initial_data.json /app/

RUN mkdir -p /vol/web/media

RUN adduser \
        --disabled-password \
        --no-create-home \
        django-user

RUN chown -R django-user:django-user /vol/
RUN chmod -R 755 /vol/web/

USER django-user