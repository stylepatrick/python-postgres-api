# set base image (host OS)
FROM python:3.8-slim

# set the working directory in the container
WORKDIR /app

# install dependencies to compile psycopg2 or use pip3 install psycopg2-binary
RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#RUN pip3 install flask
#RUN pip3 install psycopg2

COPY . .

# command to run on container start
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
