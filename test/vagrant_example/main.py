#!python3

import vagrant
from fabric.api import execute, task, local

@task
def mytask():
    local('vagrant docker-run default -- cowsay moo')

v = vagrant.Vagrant()
v.up()
execute(mytask)
v.destroy()
