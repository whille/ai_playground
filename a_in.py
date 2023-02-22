#!/usr/bin/env python
import sys
import asyncio


class AInput():
    def __init__(self):
        self.q = asyncio.Queue()

    async def out(self, prompt):
        if prompt:
            print(prompt)
        await self.q.put(sys.stdin.readline().strip())

    async def input(self, prompt='input:'):
        tasks = [self.out(prompt), self.q.get()]
        res = await asyncio.gather(*tasks)
        return res[1]


async def demo():
    ain = AInput()
    txt = await ain.input()
    print(f"got: {txt}")

if __name__ == "__main__":
    asyncio.run(demo())
