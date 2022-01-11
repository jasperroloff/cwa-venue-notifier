FROM python:3-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/app

# update package lists
RUN apk update

# configure timezone
RUN apk add --no-cache tzdata
ENV TZ Europe/Berlin

# requirements for pyscop2
RUN apk add postgresql-dev gcc python3-dev musl-dev

# postgres client (required for postgres availability detection)
RUN apk add postgresql-client

# required for compiling translation files
RUN apk add gettext-dev

# requirements for python pillow
RUN apk add freetype-dev fribidi-dev harfbuzz-dev jpeg-dev lcms2-dev openjpeg-dev tcl-dev tiff-dev tk-dev zlib-dev

# requirements for pyheif
RUN apk add libffi libffi-dev libheif libheif-dev libde265-dev

# requirements for pyzbar
RUN apk add zbar zbar-dev

# requirements for pdf2image
RUN apk add poppler-utils

# wsgi server for production deployment
RUN pip install gunicorn

# copy requirements.txt only (better for caching)
COPY requirements.txt /usr/src/app

# install pip packages
RUN pip install -r requirements.txt

# copy yarn dependencies
# COPY --from=builder-node /usr/src/app/node_modules ./node_modules

# copy project dir
COPY . /usr/src/app

# copy entrypoint
ADD .deployment/docker-entrypoint.sh /

# create package dir
RUN mkdir -p data/packages

# chmod entrypoint
RUN chmod a+x /docker-entrypoint.sh

# set port
EXPOSE 80

# set user
#USER nobody

# set entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]

# set cmd -> for webserver
#CMD ["python", "manage.py", "runserver", "[::]:80"]
CMD ["gunicorn", "cwa_venue_notifier.wsgi:application", "--bind", "[::]:80"]

# set cmd -> for celery worker ("-B" enables beat)
ENV C_FORCE_ROOT=1
#CMD ["celery", "-A", "cwa_venue_notifier", "worker", "-B", "-E", "-Q", "celery", "-l", "INFO", "-s", "/tmp/celerybeat-schedule"]

# set cmd -> for telegram bot
#CMD ["python", "manage.py", "start_polling"]
