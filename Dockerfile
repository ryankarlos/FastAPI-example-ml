FROM python:3.8-slim-bullseye AS dev
WORKDIR /usr/
# copy requirements txt files here first as they are
# less likely to me modified compared to application code
# this will prevent docker build from running all dependency
# installation everytime app code is modified (if it was copied first).
COPY src/requirements.txt /usr/src/requirements.txt
COPY src/requirements-dev.txt /usr/src/requirements-dev.txt
RUN apt-get update
RUN apt-get install -y build-essential python-dev git
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --upgrade -r /usr/src/requirements.txt \
    && pip install --no-cache-dir --upgrade -r /usr/src/requirements-dev.txt \
    && rm -rf /root/.cache/pip
COPY src/ /usr/src/
COPY tests/ /usr/tests/
ENTRYPOINT ["/bin/bash"]


FROM python:3.8-slim-bullseye AS web
WORKDIR /usr
COPY src/requirements.txt /usr/src/requirements.txt
RUN apt-get update
RUN apt-get install -y build-essential python-dev git
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir --upgrade -r /usr/src/requirements.txt \
    && rm -rf /root/.cache/pip
COPY src/app /usr/src/app
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
