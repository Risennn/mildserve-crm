# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN pip3 install pipenv
ENV PROJECT_DIR /app
COPY . /${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}

RUN pipenv install --system --deploy

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5005"]