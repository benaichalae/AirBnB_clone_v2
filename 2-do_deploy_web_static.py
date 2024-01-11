#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers."""

from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime
import os

env.hosts = ['<web_server_1_ip>', '<web_server_2_ip>']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/my_ssh_private_key'


def do_deploy(archive_path):
    """Distribute an archive to web servers."""
    if not exists(archive_path):
        return False

    try:
        put(archive_path, '/tmp/')

        filename = os.path.basename(archive_path)
        release_name = os.path.basename(archive_path).split('.')[0]
        release_folder = '/data/web_static/releases/{}'.format(release_name)
        run('mkdir -p {}'.format(release_folder))
        run('tar -xzf /tmp/{} -C {}'.format(filename, release_folder))

        run('mv {}/web_static/* {}'.format(release_folder, release_folder))
        run('rm -rf {}/web_static'.format(release_folder))

        run('rm /tmp/{}'.format(filename))

        current_link = '/data/web_static/current'
        run('rm -rf {}'.format(current_link))
        run('ln -s {} {}'.format(release_folder, current_link))

        print("New version deployed!")
        return True
    except Exception as e:
        return False


if __name__ == "__main__":
    archive_path = local("fab -f 1-pack_web_static.py do_pack", capture=True)
    archive_path = archive_path.strip()
    do_deploy(archive_path)
