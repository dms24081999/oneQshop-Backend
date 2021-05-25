# Base Image
FROM python:3.6-slim-stretch

# create and set working directory
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
# ADD . /app/
COPY ./src /app/src
COPY ./requirements.txt /app/requirements.txt
RUN pwd

ENV PORT=8888

# Install system dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    build-essential cmake \
    libopenblas-dev liblapack-dev \
    libx11-dev libgtk-3-dev \
    git \
    default-libmysqlclient-dev \
    && apt-get clean && rm -rf /tmp/* /var/tmp/* /var/lib/apt/lists/*

RUN which python3.6
RUN update-alternatives --install /usr/bin/python python /usr/local/bin/python3.6 1
RUN python -V && pip -V

# Cd into /app
RUN cd /app

# Install project dependencies
RUN pip install --upgrade pip -r requirements.txt

# run the project
EXPOSE 8888
CMD gunicorn --chdir src mainsite.wsgi:application --bind 0.0.0.0:$PORT
