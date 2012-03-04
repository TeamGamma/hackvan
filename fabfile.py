from fabric.api import *

env.hosts = ['rob@doteight.com']
remote_repo = '/srv/www/projects/apps/fountains'

def deploy():
    """ Deploys local version to server and merges into deploy branch """
    local('git push server master')
    with cd(remote_repo):
        run('git merge master')

def restart():
    """ Restart Apache """
    sudo('service apache2 restart')

