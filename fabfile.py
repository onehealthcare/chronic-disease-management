from typing import List

from fabric import SerialGroup as Group, task


UBUNTU_HOSTS: List[str] = [
    'home',
]

MACOS_HOST: List[str] = [
    '192.168.44.6'
]

HOSTS: List[str] = UBUNTU_HOSTS + MACOS_HOST


@task
def deploy(c):
    hosts: List[Group] = Group(*UBUNTU_HOSTS)
    path: str = "/home/tonghs/app/web-template"
    # git sync
    hosts.run(f'cd {path} && git checkout . && git pull --rebase')

    # TODO
    # 如果 docker 文件发生变化，重新 build

    # restart
    hosts.run(f'cd {path} && make restart', pty=True)
