FROM python:3.9.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /opt

RUN pip install --upgrade pip && pip install -r /opt/requirements.txt

EXPOSE 8000

CMD gunicorn -w 2 -b 0.0.0.0:8000 --pythonpath /opt 'app.wsgi:application'