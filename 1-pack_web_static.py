#!/usr/bin/python3
"""Deploy static"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """create .tgz with all content from web_static folder"""
    # create the folder if not exists
    local("mkdir -p versions")
    now = datetime.now()
    # create the name of the tgz
    nameTgz = "versions/web_static_"
    nameTgz += "{}{}{}".format(now.year, now.month, now.day)
    nameTgz += "{}{}{}".format(now.hour, now.minute, now.second)
    nameTgz += ".tgz"
    # command to create the tgz
    tgz_file = "tar -cvzf {} web_static".format(nameTgz)
    # return de path if the file was created
    if local(tgz_file).failed:
        return None
    return nameTgz
