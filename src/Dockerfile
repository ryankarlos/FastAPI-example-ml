FROM python:3.8.8-alpine AS dev
WORKDIR /usr/src
COPY . /usr/src
RUN apt-get update && apt-get install -y libgomp1
RUN pip install --upgrade pip setuptools wheel \
    && RUN pip install --no-cache-dir --upgrade -r /usr/src/requirements.txt \
    && RUN pip install --no-cache-dir --upgrade -r /usr/src/requirements-dev.txt \
    && rm -rf /root/.cache/pip
ENTRYPOINT ["/bin/bash"]


FROM python:3.8.8-alpine AS web
WORKDIR /usr/src

COPY ./src/requirements.txt /usr/src/requirements.txt
RUN apt-get update && apt-get install -y libgomp1
RUN pip install --upgrade pip setuptools wheel \
    && RUN pip install --no-cache-dir --upgrade -r /usr/src/requirements.txt \
    && rm -rf /root/.cache/pip
EXPOSE 8000
COPY ./src/app /usr/src/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]