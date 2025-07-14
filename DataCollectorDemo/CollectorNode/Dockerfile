# Python STAGE 1
ARG USER=uauser
ARG WORKDIR=/home/$USER/uaclient
ARG COLLECTORDIR=$WORKDIR/CollectorNode
ARG CENTRALCONFIGDIR=$COLLECTORDIR/CentralConfig
ARG OPCUACONFIGDIR=$COLLECTORDIR/OpcUaClient
ARG SERVERDIR=$COLLECTORDIR/Server
ARG BASEDIR=$WORKDIR/BaseNode
ARG COMMONDIR=$WORKDIR/Common

FROM python:3.13 AS builder

WORKDIR $WORKDIR

COPY CollectorNode/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Python STAGE 2
FROM python:3.13-slim

ARG USER
ARG WORKDIR
ARG COLLECTORDIR
ARG CENTRALCONFIGDIR
ARG OPCUACONFIGDIR
ARG SERVERDIR
ARG BASEDIR
ARG COMMONDIR

COPY --from=builder /install /usr/local

RUN useradd --create-home --uid 1000 $USER

WORKDIR $WORKDIR

COPY CollectorNode/CentralConfig $CENTRALCONFIGDIR
COPY CollectorNode/OpcUaClient $OPCUACONFIGDIR
COPY BaseNode $BASEDIR
COPY Common $COMMONDIR

COPY CollectorNode/__init__.py $COLLECTORDIR
COPY CollectorNode/__init__.py $WORKDIR
COPY CollectorNode/routes.py $COLLECTORDIR
COPY CollectorNode/main.py $COLLECTORDIR

RUN chown -R $USER $WORKDIR

USER $USER

EXPOSE 8000

CMD ["uvicorn", "CollectorNode.main:app", "--host", "0.0.0.0", "--port", "8000"]
