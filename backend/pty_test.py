import pty
import subprocess
import os
try:
    # Create a pseudo-terminal (pty) and start a shell process
    master, slave = pty.openpty()
    process = subprocess.Popen(["/bin/bash"], stdin=subprocess.PIPE,
                               stdout=slave, stderr=subprocess.STDOUT,
                               close_fds=True)

    # Send some commands to the shell process and print its output
    commands = ["ls\n", "echo 'hello world'\n", "exit\n"]
    for cmd in commands:
        process.stdin.write(cmd.encode())
        
    output, _ = process.communicate()
    if output is not None:
        print(output.decode())

except Exception as e:
    print("Error:", e)


