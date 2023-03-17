# # from sys import stdin
# # import docker
# # from docker.models.containers import Container
# # client = docker.from_env()
# # container:Container  = client.containers.run("af26f0604926","echo hello")
# # container.logs()
# # print(type(container))
# # print(container.logs())
# # a = container.exec_run("/bin/sh")
# # print(a)
# # print(container.logs())


# # import docker

# # client = docker.from_env()

# # container = client.containers.run("af26f0604926", detach=True)

# # input_data = b"hello world\n"

# # output = container.exec_run("echo", input=input_data)

# # print(output.output.decode())





# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# # import os
# # import sys
# # import select
# # import termios
# # import tty
# # import pty
# # from subprocess import Popen

# # command = 'docker run -it --rm  af26f0604926 /bin/sh'
# # # command = 'docker run -it --rm centos /bin/bash'.split()

# # # save original tty setting then set it to raw mode
# # old_tty = termios.tcgetattr(sys.stdin)
# # tty.setraw(sys.stdin.fileno())

# # # open pseudo-terminal to interact with subprocess
# # master_fd, slave_fd = pty.openpty()


# # try:
# #     # use os.setsid() make it run in a new process group, or bash job control will not be enabled
# #     p = Popen(command,
# #               preexec_fn=os.setsid,
# #               stdin=slave_fd,
# #               stdout=slave_fd,
# #               stderr=slave_fd,
# #               universal_newlines=True
# #               ,shell=True
# #             )


#     # while p.poll() is None:
#     #     r, w, e = select.select([sys.stdin, master_fd], [], [])
#     #     if sys.stdin in r:
#     #         d = os.read(sys.stdin.fileno(), 10240)
#     #         os.write(master_fd, d)
# #         elif master_fd in r:
# #             o = os.read(master_fd, 10240)
# #             if o:
# #                 os.write(sys.stdout.fileno(), o)

# # finally:
# #         # restore tty settings back
# #         termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)


# code = "print(input())"
# import pexpect
# child = pexpect.spawn('docker run -it --rm  af26f0604926 /bin/sh')
# # child.expect("/ # ")
# # child.sendline("apk add bash")
# # child.expect("\w.*")
# # child.sendline("bash")
# child.expect("\w.*")
# child.sendline("touch main.py")
# child.expect("\w.*")
# child.sendline("echo {code} > main.py")
# child.expect("\w.*")
# child.sendline("python3 main.py")
# child.sendline("5")

# child.expect("\w.*")
# print(child.before.decode())
# child.sendline("exit")
# child.expect("\w.*")
# # child.sendline("exit")
# print(child.before.decode())
# # child.kill()




async def _eval_python3(code: str, input: str, proc: asyncio.subprocess.Process):
    proc.stdin.write("touch main.py\n".encode("utf-8"))
    await proc.stdin.drain()
    proc.stdin.write(f"echo '{code}' > main.py\n".encode("utf-8"))
    await proc.stdin.drain()
    # proc.stdin.write("echo '' >> main.py\n".encode("utf-8"))  # Add newline after code
    await proc.stdin.drain()
    proc.stdin.write(f"echo '{input}' | python3 main.py\n".encode("utf-8"))
    # await proc.stdin.drain()
    # proc.stdin.write(input.encode("utf-8"))
    await proc.stdin.drain()