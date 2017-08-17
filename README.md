# docker-cmd

## Introduction

In a situation where Docker containers are started via Ansible, it can be difficult to see the command line parameters that were used to start each container, thus if we want to stop an existing container, tweak the configuration and restart, it can be difficult and time consuming to achieve this.

A Docker Inspect may be performed, but this merely returns a JSON formatted list of parameters which must be hand crafted by the user into an executable command.

This tool will inspect a running container(s) and output the command used to execute the same.

## Details

The tool is written in python, using the docker-py client API. At present it is basic and takes a number of shortcuts, but it should suffice for most use cases in rough development & test.

The tool has been built into a Pex executable so there is no need to install Python in order to run it.

```
from docker import Client
import sys
cli = Client(base_url='unix://var/run/docker.sock')
portStr = ""
mountStr = ""
imageStr = ""
nameStr = ""
envStr = ""
containerId = ""
 
 
cmdargs = str(sys.argv)
total = len(sys.argv)
if total > 1:
    containerId = sys.argv[1]
for line in cli.containers():
    portStr = ""
    mountStr = ""
    imageStr = ""
    nameStr = ""
    envStr = ""
    id = line['Id']
    if containerId != "" and not id.startswith(containerId):
        continue
    ports = line['Ports']
    if ports != []:
        for port in ports:
            if port.has_key('PublicPort') and port.has_key('PrivatePort'):
                portStr = "-p " + str(port['PublicPort']) + ":" + str(port['PrivatePort']) + " "
    mounts = line['Mounts']
    if mounts != []:
        for mount in mounts:
            mountStr += "-v " + str(mount['Source']) + ":" + str(mount['Destination']) + " "
    name = line['Names']
    if name != []:
        nameStr = "--name " + name[0].strip("/") + " "
    id = line['Id']
    if id != []:
        envs = cli.inspect_container(id)['Config']['Env']
        if envs != []:
            for env in envs:
                envStr += "-e " + str(env).replace("=", "=\"") + "\" "
    image = line['Image']   
    if image != []:
        imageStr = image
    print "docker run -d " + nameStr + portStr + mountStr + envStr + imageStr
    print ""


```

## Usage
When built into an executable with PEX the following will show details for all running containers
```

./docker_cmd

```
This returns the command for all running docker containers (separated by a single blank line) or
```

./docker_cmd <container id>

```

## Restrictions

This tools needs to be tweaked to run against versions of Docker earlier than 1.12
