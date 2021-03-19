FROM ubuntu:18.04

# MAINTAINER tonghs <tonghuashuai@gmail.com>

# 更新源 && 安装必要软件
COPY ci/sources.list /etc/apt/sources.list
COPY requirements.txt /requirements.txt
ENV DEBIAN_FRONTEND=noninteractive
RUN echo "Asia/Shanghai" > /etc/timezone && \
  apt-get update && \
  apt-get install -y software-properties-common && \
  add-apt-repository -y ppa:deadsnakes/ppa && \
  rm /usr/bin/python3 && \
  ln -s /usr/bin/python3.7 /usr/bin/python3 && \
  apt-get install -y python3.7 python3.7-dev python3-pip curl mysql-client tzdata && \
  apt-get -y autoremove --purge && \
  apt-get -y clean && apt-get -y autoclean && \
  dpkg-reconfigure -f noninteractive tzdata && \
  pip3 install -r /requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --extra-index-url https://pypi.python.org/simple --trusted-host mirrors.aliyun.com && \
  rm -rf /root/.cache && rm -rf /tmp/*

WORKDIR /opt/code/
CMD ["sh", "-c", "gunicorn app:app --bind=$GUNICORN_BIND_ADDRESS --workers=$GUNICORN_WORKERS --log-level=$GUNICORN_LOG_LEVEL $GUNICORN_RELOAD --access-logfile=$GUNICORN_ACCESS_LOGFILE --worker-class gevent"]
