import asyncio
from game.main import Game  

async def main():
    game = Game()
    await game.run()  

asyncio.run(main())