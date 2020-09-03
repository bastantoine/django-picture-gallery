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
ENV HOME=/code
RUN mkdir $HOME
RUN mkdir $HOME/staticfiles
RUN mkdir $HOME/mediafiles
WORKDIR $HOME

RUN addgroup -S webuser && adduser -S webuser -G webuser

# Copy project code.
COPY . $HOME

# chown all the files to the app user
RUN chown -R webuser:webuser $HOME

# change to the webuser user
USER webuser

# Start the server when the image is launched
ENTRYPOINT [ "./docker/prod/docker-entrypoint.prod.sh" ]
