FROM python:3.10-slim-buster

RUN pip3 install pipenv
ENV PROJECT_DIR /app
COPY . /${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}

RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 5005

CMD [ "flask", "run", "--host=0.0.0.0", "--port=5005"]