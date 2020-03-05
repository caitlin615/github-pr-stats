FROM python:3-alpine

WORKDIR /app
RUN pip install --no-cache-dir PyGithub

COPY main.py ./
CMD [ "python3", "main.py" ]
