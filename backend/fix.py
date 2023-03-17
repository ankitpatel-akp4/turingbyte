import asyncio
import aiofiles


async def eval_python3(code, input_):
    cmd = ["docker", "run", "-i", "--rm", "af26f0604926", "/bin/sh"]
    async with aiofiles.open("test.txt", "wb") as f:
        proc = await asyncio.create_subprocess_exec(*cmd, stdin=asyncio.subprocess.PIPE, stdout=f, stderr=asyncio.subprocess.PIPE)
        await asyncio.wait_for(_eval_python3(code=code, input_=input_, proc=proc), timeout=100)
        # proc.stdin.write(b"exit\n")
        await proc.stdin.drain()
        await proc.wait()
        print(proc.returncode)
    async with aiofiles.open("test.txt", "r") as f:
        print(await f.read())
    print((await proc.stderr.read()).decode())


async def _eval_python3(code, input_, proc):
    proc.stdin.write("touch main.py\n".encode())
    await proc.stdin.drain()
    proc.stdin.write(f"echo '{code}' > main.py\n".encode())
    await proc.stdin.drain()
    # proc.stdin.write("echo '' >> main.py\n".encode())  # Add newline after code
    await proc.stdin.drain()
    proc.stdin.write(f"echo '{input_}'| python3 main.py\n".encode())
   

asyncio.run(eval_python3("print(input().strip())", "hello world 5\n"))
