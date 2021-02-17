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
    results = hosts.run(f'cd {path} && git checkout . && git pull --rebase')

    if any(['Already up to date' in result.stdout for _, result in results.items()]):
        return

    # 如果 docker 文件发生变化，重新 build
    if any(['docker-compose.' in result.stdout or 'Dockerfile' in result.stdout for _, result in results.items()]):
        hosts.run(f'cd {path} && sudo -E make build-image && sudo -E make rebuild')
        return

    # restart
    hosts.run(f'cd {path} && make restart', pty=True)


@task
def restart(c):
    hosts: List[Group] = Group(*UBUNTU_HOSTS)
    path: str = "/home/tonghs/app/web-template"
    # git sync
    # hosts.run(f'cd {path} && git checkout . && git pull --rebase')

    # restart
    hosts.run(f'cd {path} && make restart', pty=True)
