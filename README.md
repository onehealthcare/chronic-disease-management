# web-template

![test](https://github.com/tonghs/web-template/workflows/test/badge.svg)  [![codecov](https://codecov.io/gh/tonghs/web-template/branch/main/graph/badge.svg?token=TTTHQMSIII)](https://codecov.io/gh/tonghs/web-template) ![build](https://github.com/tonghs/web-template/workflows/build/badge.svg)
 [![Codacy Badge](https://app.codacy.com/project/badge/Grade/763634f8270a4ceba96543bddd223592)](https://www.codacy.com/gh/tonghs/web-template/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tonghs/web-template&amp;utm_campaign=Badge_Grade)
Website template, based Python3 and Flask：
- Python3
- Flask
- Docker
- Nginx
- Gunicorn
- Sentry
- MySQL(peewee)
- Github Action
- pre-commit

## Dev
```shell
make build-image && make run-dev-server
```
配合小程序 Demo：https://github.com/tonghs/lab-x

## Online deploy
```shell
make run-server
```

## Test
```shell
make test
```
