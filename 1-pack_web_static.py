#!/usr/bin/python3
"""Fabric script to generate a .tgz archive from web_static folder."""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """Create a .tgz archive from web_static folder."""
    try:
        local("mkdir -p versions")

        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(timestamp)

        local("tar -cvzf versions/{} web_static".format(archive_name))

        return "versions/{}".format(archive_name)
    except Exception as e:
        return None
