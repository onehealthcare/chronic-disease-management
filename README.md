# web-template

![test](https://github.com/tonghs/web-template/workflows/test/badge.svg)  [![codecov](https://codecov.io/gh/tonghs/web-template/branch/main/graph/badge.svg?token=TTTHQMSIII)](https://codecov.io/gh/tonghs/web-template) ![build](https://github.com/tonghs/web-template/workflows/build/badge.svg)

集成了一些常用功能的 wesite template，基于 Python3 和 Flask，其中包括：
- Python3
- Flask
- Docker
- Nginx
- Gunicorn
- Sentry
- MySQL(peewee)
- Github Action
- pre-commit


## 开发
```shell
make build-image && make run-dev-server
```


## 线上部署
```shell
make run-server
```


## 测试
```shell
make test
```
