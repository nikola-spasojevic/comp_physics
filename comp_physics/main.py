from typing import List

import matplotlib.pyplot as plt
import pygame

from src.planet import get_planets, Planet, WIDTH, HEIGHT


pygame.init()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))


def task2(planets: List[Planet]):
    for planet in planets:
        planet.create_orbit()
    plt.show()


def task4(planets: List[Planet]):
    plt.axes(projection='3d')
    for planet in planets:
        planet.create_orbit_z()
    plt.show()


def pygame_func():
    run = True
    clock = pygame.time.Clock()

    planets: List[Planet] = get_planets()

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # planets = planets[:1] # get just mercury
        for planet in planets:
            planet.DRAW(WIN)

        pygame.display.update()
    pygame.quit()



def main():
    planets: List[Planet] = get_planets()
    task2(planets)
    task4(planets)


if __name__ == '__main__':
    main()
