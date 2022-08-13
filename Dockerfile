FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "flask", "--app", "hello", "run", "--port", "2022", "--host", "0.0.0.0"]