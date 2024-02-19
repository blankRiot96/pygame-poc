import os
import time

import colorama

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import shared
from shaders.shader import Shader

SHADERS = True
RUN_TIME_SECONDS = 5.0


class Core:
    WIN_SIZE = (800, 450)

    def __init__(self):
        self.win_init()
        self.shader_init()
        self.image = pygame.image.load("assets/images/naruto.jpg").convert()
        self.font = pygame.Font(None, 32)
        self.fps_note: list[float] = []
        self.start_time = time.perf_counter()

    def win_init(self):
        pygame.init()
        flags = pygame.OPENGL | pygame.DOUBLEBUF if SHADERS else 0
        pygame.display.set_mode(Core.WIN_SIZE, flags=flags)
        shared.win = (
            pygame.Surface(Core.WIN_SIZE, pygame.SRCALPHA)
            if SHADERS
            else pygame.display.get_surface()
        )
        shared.WRECT = shared.win.get_rect()
        self.clock = pygame.Clock()

    def shader_init(self):
        if not SHADERS:
            return
        self.display_shader = Shader(
            vert_shader_name="vert", frag_shader_name="display"
        )

    def end(self) -> None:
        msg_format = "FPS OBTAINED WITH SHADERS {on_off} FOR {blue}{runtime:.2f}s{reset} IS {green}{average_fps:.2f}{reset}"
        print(
            msg_format.format(
                on_off="ON" if SHADERS else "OFF",
                runtime=time.perf_counter() - self.start_time,
                average_fps=sum(self.fps_note) / len(self.fps_note),
                green=colorama.Fore.GREEN,
                blue=colorama.Fore.BLUE,
                reset=colorama.Fore.RESET,
            )
        )
        raise SystemExit

    def traverse_events(self):
        for event in shared.events:
            if event.type == pygame.QUIT:
                self.end()

    def update(self):
        shared.dt = self.clock.tick() / 1000
        shared.events = pygame.event.get()
        shared.keys = pygame.key.get_pressed()

        self.traverse_events()
        if SHADERS:
            self.display_shader.update()

        if time.perf_counter() - self.start_time > RUN_TIME_SECONDS:
            self.end()

    def render(self):
        shared.win.fill("black")
        shared.win.blit(self.image, self.image.get_rect(center=shared.WRECT.center))
        fps = self.clock.get_fps()
        fps_surf = self.font.render(f"{fps:.2f}", True, "green")
        self.fps_note.append(fps)
        shared.win.blit(fps_surf, (0, 0))
        if SHADERS:
            self.display_shader.pass_surf_to_gl(shared.win)
            self.display_shader.render()

        pygame.display.flip()

    def run(self):
        while True:
            self.update()
            self.render()


def main():
    core = Core()
    core.run()


if __name__ == "__main__":
    main()
