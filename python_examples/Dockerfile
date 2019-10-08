FROM python:3.7.4

ENV TZ=Africa/Accra

RUN apt-get update \
    && apt-get install -y cron \
    && apt-get autoremove -y

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY ./cronpy /etc/cron.d/cronpy

CMD ["cron", "-f"]
