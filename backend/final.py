from subprocess import Popen, PIPE
import select

process = Popen("docker exec -i 8e4a030f1620 /bin/sh"
                ,shell=True, text=True
                ,stdin=PIPE, stdout=PIPE, stderr=PIPE)

code = """
print("welcome")
name = input("What is your name: ")
print(f"Hello \{name\}")
"""
stdin = process.stdin
stdout = process.stdout
stderr = process.stderr

stdin.write("echo python3 -c {code} | xargs | echo && echo \n")
stdin.flush()
while True:
    r, w, e = select.select([stdout],[],[],.1)
    if r:
        output = stdout.readline()
        if output == "":
            break
print(output.encode())
stdin.write("John\n")
stdin.flush()
process.wait()
