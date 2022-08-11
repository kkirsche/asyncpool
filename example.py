import asyncpool
import logging
import asyncio

async def example_coro(initial_number, result_queue):
    print(f"Processing Value! -> {initial_number} * 2 = {initial_number * 2}")
    await asyncio.sleep(1)
    await result_queue.put(initial_number * 2)

async def result_reader(queue):
    while True:
        value = await queue.get()
        if value is None:
            break
        print(f"Got value! -> {value}")

async def run():

    result_queue = asyncio.Queue()

    reader_future = asyncio.ensure_future(result_reader(result_queue), loop=loop)

    # Start a worker pool with 10 coroutines, invokes `example_coro` and waits for it to complete or 5 minutes to pass.
    async with asyncpool.AsyncPool(loop, num_workers=10, name="ExamplePool",
                             logger=logging.getLogger("ExamplePool"),
                             worker_co=example_coro, max_task_time=300,
                             log_every_n=10) as pool:
        for i in range(50):
            await pool.push(i, result_queue)

    await result_queue.put(None)
    await reader_future

loop = asyncio.get_event_loop()

loop.run_until_complete(run())