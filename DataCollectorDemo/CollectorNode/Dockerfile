# Python STAGE 1
ARG USER=uauser
ARG WORKDIR=/home/$USER/uaclient

FROM python:3.13 AS builder

WORKDIR $WORKDIR

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Python STAGE 2
FROM python:3.13-slim

ARG USER
ARG WORKDIR

COPY --from=builder /install /usr/local

WORKDIR $WORKDIR

COPY CentralConfig $WORKDIR/CentralConfig
COPY OpcUaClient $WORKDIR/OpcUaClient
COPY Server $WORKDIR/Server
COPY ../Common $WORKDIR/../Common

COPY main.py .

EXPOSE 8000

CMD ["python", "main.py"]
