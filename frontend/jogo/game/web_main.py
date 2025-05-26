import asyncio
import pygame as pg
from main import Game
from settings import fps

class WebGame(Game):
    async def run(self):
        """Versão adaptada do loop principal para web"""
        while True:
            if not self.running:
                self.menu.handle_events()
                self.menu.draw()
            else:
                self.check_events()    
                if not self.paused:
                    self.update()
                self.draw()

            pg.display.flip()
            self.delta_time = self.clock.tick(fps)
            await asyncio.sleep(0)  # Crucial para a web

async def main():
    game = WebGame()
    await game.run()

asyncio.run(main())