FROM python:3.8.5-alpine

# Set environment variables
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
# https://github.com/psycopg/psycopg2/issues/684
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev

COPY requirements.txt /

# Install dependencies.
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# Set work directory.
RUN mkdir /code
WORKDIR /code

# Copy project code.
COPY . /code/

EXPOSE 8080

# Start the server when the image is launched
ENTRYPOINT [ "./docker-entrypoint.sh" ]
