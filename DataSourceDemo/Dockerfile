ARG USER=serverurser
ARG WORKDIR=/home/$USER/server

# Python STAGE 1
FROM python:3.13 AS builder

WORKDIR $WORKDIR

# Setup the required packages
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Python STAGE 2
FROM python:3.13

ARG USER
ARG WORKDIR

# copy the installed Python modules
COPY --from=builder /install /usr/local

WORKDIR $WORKDIR

# install the own modules
COPY main.py .
COPY MyServer $WORKDIR/MyServer

# do NOT run as root
RUN useradd -m -d /home/$USER $USER
USER $USER

# Ports to expose, we are using a OPC UA server here
EXPOSE 4840, 8765

CMD ["python", "main.py"]
