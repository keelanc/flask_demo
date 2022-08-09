# set base image (host OS)
FROM python:alpine3.10

# set the working directory in the container
WORKDIR /api

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY ./src_api /api/src_api
COPY ./tests /api/tests

ENV PYTHONPATH=/api

# Expose port 5000
EXPOSE 5000