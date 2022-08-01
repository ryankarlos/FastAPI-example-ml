FROM python:3.8-slim-bullseye AS dev
WORKDIR /usr/src
# copy requirements txt files here first as they are
# less likely to me modified compared to application code
# this will prevent docker build from running all dependency
# installation everytime app code is modified (if it was copied first).
COPY requirements.txt /usr/src/requirements.txt
COPY requirements-dev.txt /usr/src/requirements-dev.txt
RUN apt-get update
RUN apt-get install -y build-essential python-dev git
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --upgrade -r /usr/src/requirements.txt \
    && pip install --no-cache-dir --upgrade -r /usr/src/requirements-dev.txt \
    && rm -rf /root/.cache/pip
COPY . /usr/src/
ENTRYPOINT ["/bin/bash"]


FROM python:3.8-slim-bullseye AS web
WORKDIR /usr
COPY requirements.txt /usr/src/requirements.txt
RUN apt-get update
RUN apt-get install -y build-essential python-dev git
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --upgrade -r /usr/src/requirements.txt \
    && rm -rf /root/.cache/pip
COPY ./app /usr/src/app
EXPOSE 80
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
