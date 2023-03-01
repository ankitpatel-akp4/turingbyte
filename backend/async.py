import  asyncio
import uvloop
import datetime
import threading
# uvloop.install()
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# def trampoline(name:str = "")-> None:
#     print(name,end=" ")
#     print_now()
#     loop.call_later(0.5,trampoline,name)
# # # loop.run_forever()
def print_now():
    print(datetime.datetime.now())
# loop.call_soon(trampoline)
# loop.call_later(8,loop.stop)
# loop.run_forever()
# loop.call_soon(print_now)

# loop.run_until_complete(asyncio.sleep(5))


# async def keep_printing(name):
#     while True:
#         print(name,end=" ")
#         print(threading.current_thread().name)
#         print_now()
#         await asyncio.sleep(.5)



# async def async_main() -> None:
#     try:
#         await asyncio.wait_for(keep_printing("amin"),10)
#     except asyncio.TimeoutError:
#         print("opps, time's up")

# asyncio.run(async_main())

async def time(name):
    print(threading.current_thread().name)
    print(name,datetime.datetime.now())

def blockeint():
    print(threading.current_thread().name)
    print(datetime.datetime.now())

async def main():
    await asyncio.gather(
        time("a"),
        time("B"),
        asyncio.to_thread(blockeint)

    )

asyncio.run(main())
