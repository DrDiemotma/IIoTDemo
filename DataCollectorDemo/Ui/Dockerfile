# Python STAGE 1
ARG USER=uiuser
ARG WORKDIR=/home/$USER/uiservice
ARG SERVICEDIR=$WORKDIR/Ui
ARG COMMONDIR=$WORKDIR/Common

FROM python:3.13 AS builder

WORKDIR $WORKDIR

COPY Ui/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Python STAGE 2
FROM python:3.13-slim

ARG USER
ARG WORKDIR
ARG SERVICEDIR
ARG COMMONDIR

COPY --from=builder /install /usr/local
RUN useradd --create-home --uid 1000 $USER

WORKDIR $WORKDIR

COPY Common $COMMONDIR

COPY Ui/Frames $SERVICEDIR/Frames
COPY Ui/Communication $SERVICEDIR/Communication
COPY Ui/main.py $SERVICEDIR
COPY Ui/__init__.py $SERVICEDIR
COPY Ui/__init__.py $WORKDIR
# COPY ../CollectorNode/CentralConfig $WORKDIR/../CollectorNode/CentralConfig

RUN chown -R $USER $WORKDIR

USER $USER

EXPOSE 8501

ENV PYTHONPATH=$WORKDIR

ENTRYPOINT ["streamlit", "run", "Ui/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
