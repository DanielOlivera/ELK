FROM python:3.10-slim-buster
WORKDIR /usr/src/app
RUN apt-get update && \
	apt-get install -y curl && \
	curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN python3.10 -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./app.py" ]
