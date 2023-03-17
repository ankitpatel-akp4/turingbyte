import docker
import os
import pty
from docker.models.containers import Container
client = docker.from_env()

# cntr = client.containers.run("af26f0604926"
# ,"/bin/sh"
#  ,detach=True
# #  ,auto_remove=True
#  ,tty=True,
#  entrypoint='tail -f /dev/null',
#  )

# client.containers.prune()


# cntr_list = client.containers.list(all=True)

# for cntr in cntr_list:
    
    # cntr.stop()
    # cntr.start()
    # print(cntr.id)

# cntr_list = client.containers.list(all=True)
# print(cntr_list) 

# for line in cntr
# a = client.images.get("af26f0604926")
# master_fd, slave_fd = pty.openpty()
# container = client.containers.get(container_id="8e4a030f1620")
# cntr.start()
# print(cntr.logs())
# print(cntr.status)
# res = cntr.exec_run("python3")
# print(res)
# print(cntr.status)



import os

# Create a pseudo-terminal
master_fd, slave_fd = os.openpty()

# Attach to the container
container = client.containers.get('8e4a030f1620')
cmd = ['/bin/sh']
exec_id = container.exec_run(cmd, tty=True, stdin=True, stdout=True, stderr=True)
os.set_blocking(master_fd, False)
os.set_blocking(slave_fd, False)
proc = container.exec_start(exec_id['Id'], detach=True, tty=True)

# Write input to the process running inside the container
input_data = 'echo "Hello, world!"\n'
os.write(master_fd, input_data.encode())

# Read output from the process running inside the container
output_data = b''
while True:
    try:
        data = os.read(master_fd, 1024)
        if not data:
            break
        output_data += data
    except OSError:
        pass

print(output_data.decode())






# client = docker.from_env()
# container = client.containers.run('image_name', detach=True)

# # Attach to the container's terminal and create a pseudo-terminal
# stream = container.attach(stdout=True, stderr=True, stream=True)
# master_fd, slave_fd = pty.openpty()

# # Start an interactive shell in the container
# cmd = 'bash -i'
# container.exec_run(cmd, tty=True, stdin=True, stdout=slave_fd, stderr=slave_fd)

## Read user input and send it to the container
# while True:
#     try:
#         user_input = os.read(master_fd, 1024).decode()
#         stream.write(user_input.encode())
#     except OSError:
#         break

# Close the pseudo-terminal and stream
# os.close(master_fd)
# os.close(slave_fd)
# stream.close()


# print(4)
# print(cntr)
# print("hlllo ")

# for item in range(10):
#  print(item)

