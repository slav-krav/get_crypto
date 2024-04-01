FROM python:3.11-alpine

RUN adduser -D worker
USER worker
WORKDIR /home/worker
ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker src/ src/
COPY --chown=worker:worker requirements.txt .

RUN pip install -r requirements.txt

WORKDIR src
