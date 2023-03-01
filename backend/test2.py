# import test
# a = test.A()
# print(a.c)
# # print(a.__a)

import asyncio
import contextvars
import time

class Task:
    def __init__(self, coro):
        ...
        # Get the current context snapshot.
        self._context = contextvars.copy_context()
        self._loop.call_soon(self._step, context=self._context)

    def _step(self, exc=None):
        ...
        # Every advance of the wrapped coroutine is done in
        # the task's context.
        self._loop.call_soon(self._step, context=self._context)

# declare context var
current_request_id_ctx = contextvars.ContextVar('',default=1)
current_request_id_global = ''


async def some_inner_coroutine():
    global current_request_id_global

    # simulate some async work
    await asyncio.sleep(1)

    # get value
    # print('Processed inner coroutine of request: {}'.format(current_request_id_ctx.get()))
    # if current_request_id_global != current_request_id_ctx.get():
    print(f"ERROR! global var={current_request_id_global}")
    print('Processed outer coroutine of request: {}\n'.format(current_request_id_ctx.get()))



async def some_outer_coroutine(req_id):
    global current_request_id_global

    # set value
    current_request_id_ctx.set(req_id)
    current_request_id_global = req_id

    await some_inner_coroutine()
    await read()
    # get value

    # print('Processed outer coroutine of request: {}\n'.format(current_request_id_ctx.get()))


async def main():
    tasks = []
    for req_id in range(1, 5):
        
        tasks.append(asyncio.create_task(some_outer_coroutine(req_id)))

    await asyncio.gather(*tasks)
    

async def read():
    for i in range(1,10):
        print("read ",current_request_id_ctx.get())

if __name__ == '__main__':
    asyncio.run(main())