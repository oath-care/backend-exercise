FROM python:3.7

ENV PYTHONUNBUFFERED 1
ENV DOCKER_CONTAINER 1

RUN apt-get update

# copy source, install dependencies, and apply Django migrations
COPY .pip_cache /src/pip_cache/
COPY . /src/
WORKDIR /src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir -p /var/tmp/django_cache
RUN python manage.py makemigrations --noinput && python manage.py migrate

EXPOSE 8000
STOPSIGNAL SIGTERM

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
