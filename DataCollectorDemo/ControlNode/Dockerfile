# this script assumes that it is called from the main directory.

ARG USER=controlserver
ARG WORKDIR=/home/$USER/Service/
ARG CONTROLDIR=$WORKDIR/ControlNode/
ARG BASEDIR=$WORKDIR/BaseNode/
ARG COMMONDIR=$WORKDIR/Common/

FROM python:3.13 as builder

WORKDIR $WORKDIR

COPY ControlNode/requirements.txt $WORKDIR
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Python stage 2
FROM python:3.13-slim

ARG USER
ARG WORKDIR
ARG CONTROLDIR
ARG BASEDIR
ARG APPLICATION
ARG COMMONDIR

COPY --from=builder /install /usr/local

# create the local user
RUN useradd --create-home --uid 1000 $USER

WORKDIR $WORKDIR

COPY BaseNode/ $BASEDIR
COPY Common/ $COMMONDIR
COPY ControlNode/Server/* $CONTROLDIR/Server/

COPY ControlNode/main.py $CONTROLDIR

COPY ControlNode/__init__.py $CONTROLDIR
COPY ControlNode/__init__.py $WORKDIR
COPY ControlNode/routes.py $CONTROLDIR

# give them the work directory
RUN chown -R $USER $WORKDIR

# Now switch to the user
USER $USER

EXPOSE 8000

CMD ["uvicorn", "ControlNode.main:app", "--host", "0.0.0.0", "--port", "8000" ]
