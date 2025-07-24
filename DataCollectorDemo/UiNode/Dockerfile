# this script assumes that it is called from the main directory.

ARG USER=uiuser
ARG WORKDIR=/home/$USER/Service
ARG COMMONDIR=$WORKDIR/Common
ARG BASEDIR=$WORKDIR/BaseNode

FROM python:3.13 as builder

WORKDIR $WORKDIR

COPY UiNode/requirements.txt $WORKDIR
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.13-slim

ARG USER
ARG WORKDIR
ARG COMMONDIR
ARG BASEDIR

COPY --from=builder /install /usr/local

RUN useradd --create-home --uid 1000 $USER

WORKDIR $WORKDIR

COPY Common/ $COMMONDIR
COPY BaseNode/ $BASEDIR
COPY UiNode/UiServer/* $WORKDIR/UiServer

COPY UiNode/__init__.py $WORKDIR
COPY UiNode/__init__.py $WORKDIR
COPY UiNode/main.py $WORKDIR

RUN chown -R $USER $WORKDIR

EXPOSE 8012

CMD ["uvicorn", "UiNode.main:app", "--host", "0.0.0.0", "--port", "8012"]
