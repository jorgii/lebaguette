FROM python:3.7

ARG SRC_DIR_NAME=source

# Set environmental variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=lebaguette.settings

# Add main app source code
COPY ./ /${SRC_DIR_NAME}

# Install requirements
RUN pip install --no-cache-dir \
  uwsgi \
  -r /${SRC_DIR_NAME}/requirements.txt

WORKDIR /${SRC_DIR_NAME}

CMD ["uwsgi", "--http", "0.0.0.0:8000", "--wsgi-file", "lebaguette/wsgi.py"]
