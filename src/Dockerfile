# pull official base image
FROM python:3.8.8-alpine

# set work directory
WORKDIR /code

# copy requirements file
COPY ./requirements.txt /code/requirements.txt

# install dependencies
RUN apt-get update && apt-get install -y libgomp1
RUN pip install --upgrade pip setuptools wheel \
    && RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]