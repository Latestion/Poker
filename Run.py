import subprocess
import asyncio

async def run():
    for _ in range(500):
        subprocess.run(["python", "Game.py"])

async def main():
    await asyncio.gather(run(), run(), run(), run())

# asyncio.run(main())
d = {"wins": 0, "draws": 0, "loss": 0}
x = {3: "test"}

x[3] = "u"
print(x)

print(d)
d["wins"] += 1
print(d)