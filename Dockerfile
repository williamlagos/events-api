FROM ubuntu:latest

EXPOSE 8000

RUN apt update
RUN apt install -y python2 python2-dev build-essential curl git
RUN curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py
RUN python2 get-pip.py
RUN pip install pylint
RUN pip install -r requirements.txt
RUN python2 manage.py collectstatic --noinput
RUN python2 manage.py migrate

CMD ["python2", "manage.py", "runserver", "0.0.0.0:8000"]