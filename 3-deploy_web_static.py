#!/usr/bin/python3
"""Deploy static"""
from fabric.api import local, put, run, env
from datetime import datetime
from os.path import isfile
env.hosts = ["34.229.141.135", "52.91.220.53"]
env.key_filename = "~/.ssh/id_rsa"
env.user = "ubuntu"


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


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    # if the path doesn't exists
    if isfile(archive_path) is False:
        return False
    # try to do all the commands
    try:
        # full_name has extension, fileName no, only the name
        full_name = archive_path.split("/")[1]
        fileName = archive_path.split("/")[1].split(".")[0]

        # upload the archive_path in /tmp/
        put(archive_path, "/tmp/{}".format(full_name))

        # create the directory where are going to be uncompress
        command = "mkdir -p /data/web_static/releases/{}/".format(fileName)
        run(command)

        # uncompress the file into /data/web_static/releases/
        command = "tar -xzf /tmp/{} -C ".format(full_name)
        command += "/data/web_static/releases/{}/".format(fileName)
        run(command)

        # delete file from server
        command = "rm /tmp/{}".format(full_name)
        run(command)

        # move all the files into the dir releases/web_static<number>
        command = "mv /data/web_static/releases/{}".format(fileName)
        command += "/web_static/* "
        command += "/data/web_static/releases/{}/".format(fileName)
        run(command)

        # delete the folder that create the uncompres process
        command = "rm -rf /data/web_static/releases/{}".format(fileName)
        command += "/web_static"
        run(command)

        # delete the symbolic link
        command = "rm -rf /data/web_static/current"
        run(command)

        # create the new symbolic link
        command = "ln -s /data/web_static/releases/{}/ ".format(fileName)
        command += "/data/web_static/current"
        run(command)
    except Exception:
        # return false if it fails
        return False
    # return true if all run good
    return True


def deploy():
    """creates and distributes an archive to the web servers"""
    # compress all the information and get the name of the .tgz
    archive_path = do_pack()
    # if the archive is None
    if archive_path is None:
        return False
    # return the result
    return do_deploy(archive_path)
