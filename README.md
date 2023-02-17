# web-template

![build](https://github.com/onehealthcare/chronic-disease-management/actions/workflows/test_and_build_image.yml/badge.svg)
![CodeFactor](https://www.codefactor.io/repository/github/onehealthcare/chronic-disease-management/badge)
![codecov](https://codecov.io/gh/onehealthcare/chronic-disease-management//branch/main/graph/badge.svg?token=TTTHQMSIII)

[//]: # ([![Codacy Badge]&#40;https://app.codacy.com/project/badge/Grade/763634f8270a4ceba96543bddd223592&#41;]&#40;https://www.codacy.com/gh/tonghs/web-template/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tonghs/web-template&amp;utm_campaign=Badge_Grade&#41;)

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
