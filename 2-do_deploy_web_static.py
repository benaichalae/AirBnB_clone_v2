#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers"""
from datetime import datetime
from fabric.api import env, local, put, run
import os

env.hosts = ["34.224.3.203", "100.25.143.92"]
env.user = "ubuntu"


def do_pack():
    """generate tgz"""
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    archived_f_path = "versions/web_static_{}.tgz".format(date)
    t_gzip_archive = local("tar -cvzf {} web_static".format(archived_f_path))

    return archived_f_path if t_gzip_archive.succeeded else None


def do_deploy(archive_path):
    """deploy archive to server"""
    if os.path.exists(archive_path):
        filename = os.path.basename(archive_path)
        release_folder = "/data/web_static/releases/{}".format(filename[:-4])
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(release_folder))
        run("sudo tar -xzf /tmp/{} -C {}/".format(filename, release_folder))
        run("sudo rm /tmp/{}".format(filename))
        run("sudo mv {}/web_static/* {}".format(release_folder,
            release_folder))
        run("sudo rm -rf {}/web_static".format(release_folder))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(release_folder))

        print("New version deployed!")
        return True

    return False
