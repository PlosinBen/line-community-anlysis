#FROM python:alpine3.14
FROM python:3.10

WORKDIR /app

#COPY requirements.txt /app/requirements.txt
#RUN pip install -r requirements.txt
RUN apk add font-isas-misc &&  \
    pip install --upgrade pip setuptools &&  \
    #pip install -U git+https://github.com/p208p2002/ckiptagger@ckiptagger-tf2.1 && \
    #pip install -U ckiptagger[tf,gdown] && \
    pip install jieba wordcloud python-dotenv && \
    pip cache remove *

# Now copy in our code, and run it
#COPY . /app

#ENTRYPOINT ["tail", "-f", "/dev/null"]
