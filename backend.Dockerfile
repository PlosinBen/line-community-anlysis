#FROM python:alpine3.14
FROM python:3.10

WORKDIR /app

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools && pip install -r requirements.txt

# Now copy in our code, and run it
#COPY . /app

#ENTRYPOINT ["tail", "-f", "/dev/null"]
