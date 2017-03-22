import netrc
import os
import shutil
import sys
import SocketServer

from fabric.api import *
import fabric.contrib.project as project

import ftputil
import logging
logging.basicConfig(filename='fabric.log', level=logging.DEBUG, format='%(levelname)s -> %(asctime)s ->  %(message)s')

from pelican.server import ComplexHTTPRequestHandler

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration
production = 'root@localhost:22'
dest_path = '/var/www'

# Rackspace Cloud Files configuration settings
env.cloudfiles_username = 'my_rackspace_username'
env.cloudfiles_api_key = 'my_rackspace_api_key'
env.cloudfiles_container = 'my_cloudfiles_container'

# Github Pages configuration
env.github_pages_branch = "gh-pages"

# Port for `serve`
PORT = 8000

def clean():
    """Remove generated files"""
    if os.path.isdir(DEPLOY_PATH):
        shutil.rmtree(DEPLOY_PATH)
        os.makedirs(DEPLOY_PATH)

def build():
    """Build local version of site"""
    local('pelican -s pelicanconf.py')

def rebuild():
    """`build` with the delete switch"""
    local('pelican -d -s pelicanconf.py')

def regenerate():
    """Automatically regenerate site upon file modification"""
    local('pelican -r -s pelicanconf.py')

def serve():
    """Serve site at http://localhost:8000/"""
    os.chdir(env.deploy_path)

    class AddressReuseTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

    server = AddressReuseTCPServer(('', PORT), ComplexHTTPRequestHandler)

    sys.stderr.write('Serving on port {0} ...\n'.format(PORT))
    server.serve_forever()

def reserve():
    """`build`, then `serve`"""
    build()
    serve()

def preview():
    """Build production version of site"""
    local('pelican -s publishconf.py')

def cf_upload():
    """Publish to Rackspace Cloud Files"""
    rebuild()
    with lcd(DEPLOY_PATH):
        local('swift -v -A https://auth.api.rackspacecloud.com/v1.0 '
              '-U {cloudfiles_username} '
              '-K {cloudfiles_api_key} '
              'upload -c {cloudfiles_container} .'.format(**env))

@hosts(production)
def publish():
    """Publish to production via rsync"""
    local('pelican -s publishconf.py')
    project.rsync_project(
        remote_dir=dest_path,
        exclude=".DS_Store",
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True,
        extra_opts='-c',
    )

def gh_pages():
    """Publish to GitHub Pages"""
    rebuild()
    local("ghp-import -b {github_pages_branch} {deploy_path} -p".format(**env))

def ftp_upload():
    netrc_data = netrc.netrc(env.netrc_file)
    authenticator = netrc_data.authenticators(env.ftp_host)

    def upload_dir(source, target):
        ftp_host.chdir(target)
        for dir_name, _, dir_fiels in os.walk(source):

            local = os.path.join(os.curdir, dir_name)
            local_strip = local.strip("./")
            local_for_remote = local_strip.strip(source)
            if not ftp_host.path.exists(target + local_for_remote):
                ftp_host.makedirs(target + local_for_remote)

            for file_ in os.listdir(local_strip):
                source_upload = local + "/" + file_
                target_upload = target + local_for_remote +"/" + file_
                if not os.path.isdir(source_upload):
                    logging.debug("uploads {},  {}".format(source_upload, target_upload))
                    ftp_host.upload(source_upload, target_upload)

    with ftputil.FTPHost(env.ftp_host, authenticator[0], authenticator[2]) as ftp_host:
        upload_dir(env.deploy_path, env.ftp_target_dir)
