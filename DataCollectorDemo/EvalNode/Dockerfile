ARG USER=eval
ARG WORKDIR=/home/$USER/evaluation_node

FROM python:3.13

WORKDIR $WORKDIR

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.13-slim

ARG USER
ARG WORKDIR

COPY --from=builder /install /usr/local

WORKDIR $WORKDIR

COPY main.py .

RUN useradd -m -d /home/$USER $USER
USER $USER

CMD ["python", "main.py"]
