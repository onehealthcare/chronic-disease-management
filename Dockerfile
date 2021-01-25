FROM ubuntu:18.04

MAINTAINER tonghs <tonghuashuai@gmail.com>

# 更新源 && 安装必要软件
# COPY sources.list /etc/apt/sources.list
# RUN apt-get update && apt-get install software-properties-common -y && add-apt-repository -y ppa:deadsnakes/ppa && apt-get install python-pip python-dev python3.7 python3-dev python3-pip libmysqlclient-dev -y
RUN apt-get update && apt-get install software-properties-common -y && add-apt-repository -y ppa:deadsnakes/ppa && apt-get install python3.7 python3-dev python3-pip curl -y

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

CMD ["python3", "/opt/code/app.py"]

