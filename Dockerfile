FROM williamlagos/python_vscode:2

WORKDIR /app
ADD . /app

ENV DANCEAPP_ENVIRONMENT 1

RUN apt update
RUN apt install -y python2 python2-dev postgresql-server-dev-12 build-essential curl git
# RUN curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py
# RUN python2 get-pip.py
# RUN pip install pylint
RUN pip install -r requirements.txt
RUN python2 manage.py collectstatic --noinput
RUN python2 manage.py migrate

# CMD ["python2", "manage.py", "runserver", "0.0.0.0:8000"]
CMD gunicorn --bind 0.0.0.0:$PORT danceapp.wsgi 