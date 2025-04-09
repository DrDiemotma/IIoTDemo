# Python STAGE 1
ARG USER=uauser
ARG WORKDIR=/home/$USER/uaclient

FROM python:3.13 AS builder

WORKDIR $WORKDIR

COPY Requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r Requirements.txt

# Python STAGE 2
FROM python:3.13-slim

ARG USER
ARG WORKDIR

COPY --from=builder /install /usr/local

WORKDIR $WORKDIR

COPY main.py .
COPY Frames $WORKDIR/Frames
COPY Communication $WORKDIR/Communication
COPY ../Common $WORKDIR/../Communication
# COPY ../CollectorNode/CentralConfig $WORKDIR/../CollectorNode/CentralConfig

RUN useradd -m -d /home/$USER $USER
USER $USER

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port8501", "--server.address=0.0.0.0"]
