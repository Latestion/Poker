import subprocess
import asyncio

async def run():
    for _ in range(500):
        subprocess.run(["python", "Game.py"])

async def main():
    await asyncio.gather(run(), run(), run(), run())

asyncio.run(main())

