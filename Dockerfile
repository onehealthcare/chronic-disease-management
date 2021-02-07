FROM ubuntu:18.04

MAINTAINER tonghs <tonghuashuai@gmail.com>

# 更新源 && 安装必要软件
COPY ci/sources.list /etc/apt/sources.list
# RUN apt-get update && apt-get install software-properties-common -y && add-apt-repository -y ppa:deadsnakes/ppa && apt-get install python-pip python-dev python3.7 python3-dev python3-pip libmysqlclient-dev -y
RUN apt-get update && apt-get install software-properties-common -y && add-apt-repository -y ppa:deadsnakes/ppa && rm /usr/bin/python3 && ln -s /usr/bin/python3.7 /usr/bin/python3 && apt-get install python3.7 python3.7-dev python3-pip curl mysql-client -y  && apt-get autoclean

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --extra-index-url https://pypi.python.org/simple --trusted-host mirrors.aliyun.com

WORKDIR /opt/code/
CMD ["sh", "-c", "gunicorn app:app --bind=$GUNICORN_BIND_ADDRESS --workers=$GUNICORN_WORKERS --log-level=$GUNICORN_LOG_LEVEL $GUNICORN_RELOAD --access-logfile=$GUNICORN_ACCESS_LOGFILE --worker-class gevent"]
