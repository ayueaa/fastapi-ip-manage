FROM python:3.9.10-slim

ENV PYTHONUNBUFFERED 1

EXPOSE 8080

WORKDIR /opt/myapp
COPY . ./


RUN sed -i "s@http://deb.debian.org@https://mirrors.ustc.edu.cn@g" /etc/apt/sources.list \
    && sed -i "s@http://security.debian.org@https://mirrors.ustc.edu.cn@g" /etc/apt/sources.list \
    && apt-get update  \
    && apt-get install -y vim inetutils-ping net-tools busybox \
	&& rm -rf /var/lib/apt/lists/* /var/tmp/*\
    && echo "Asia/Shanghai" > /etc/timezone \
	&& ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

RUN set -x \
	&& pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ \
	&& chmod -R a+x scripts

ENV APP_ENV=dev

CMD uvicorn --host=0.0.0.0 --port=8080 app.main:app
