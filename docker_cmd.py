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