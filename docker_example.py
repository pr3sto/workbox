import sys
from docker import Client

client = Client()
client.login("username", password="password", registry="localhost:5000")

print(client.info())

print(client.containers())

container_id = client.create_container(image='localhost:5000/whalesay', command='cowsay hello from docker')
client.start(container_id)

for log in client.logs(container_id, stream=True):
    sys.stdout.write(log)#print(log)

client.remove_container(container_id)
