from typing import List

import pygame
import matplotlib.pyplot as plt


from src.planet import get_planets, Planet, WIDTH, HEIGHT


def task1(planets: List[Planet]):
    semi_major_axis_three_over_two = []
    orbital_periods = []
    for planet in planets:
        semi_major_axis_three_over_two.append(planet.semi_major_axis ** (3/2))
        orbital_periods.append(planet.orbital_period)
    
    plt.title("Kepler's Third Law")
    plt.xlabel('(a / AU) * (3/2)')
    plt.ylabel('T /Yr')
    plt.plot(semi_major_axis_three_over_two,orbital_periods)
    plt.scatter(semi_major_axis_three_over_two,orbital_periods, 10, 'Red')
    plt.show()


def task2(planets: List[Planet]):
    for planet in planets:
        planet.create_orbit()
    plt.show()


def task4(planets: List[Planet]):
    plt.axes(projection='3d')
    #planets = planets [:4]
    for planet in planets:
        planet.create_orbit_z()
    plt.show()


def task3():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    run = True
    clock = pygame.time.Clock()

    planets: List[Planet] = get_planets()
    frames = 0

    if input("first four?")[0] == 'y':
        planets = planets[:4]
        for planet in planets:
            planet.SCALE = 150/Planet.AU
    else:
        planets = planets[4:]


    outer_line_coordinates, outer_locations = planets[-1].create_orbit()

    while run and frames < planets[-1].ten_rotations_frames_time():
        clock.tick(60)
        WIN.fill((0,0,0))
        # pygame.display.update()
        frames += 1 #increases by one every frame, counting them

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            togethercoords, locations = planet.create_orbit()
            #locations = planet.increase_locations(planets[-1])
            planet.DRAW(WIN, locations[frames])
            if frames > len(outer_locations) / 60 and run:
                print ("Program closed as a rotation of the outer planet happened")
                run = False
            pygame.draw.lines(WIN, planet.color, False, togethercoords, 2)

        pygame.display.update()
        # WIN.fill((0,0,0))

    pygame.quit()



def task5():
    planets: List[Planet] = get_planets()
    planets = planets[:1]
    for planet in planets:
        Planet.time_at_certain_angles(planet)


def task6():
    import pygame
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    WIN.fill((255,255,255))
    run = True
    clock = pygame.time.Clock()

    planets: List[Planet] = get_planets()

    planets = [planets[1],planets[2]]
    frames = 0

    while run and frames < planets[1].ten_rotations_frames_time():
        #print (planets[1].ten_rotations_frames())
        clock.tick(60)
        pygame.display.update()
        frames += 1 #increases by one every frame, counting them

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        togethercoords, locations = planets[0].create_orbit()
        pygame.draw.lines(WIN, planets[0].color, False, togethercoords, 2)
        togethercoords, locations = planets[1].create_orbit()
        pygame.draw.lines(WIN, planets[1].color, False, togethercoords, 2)
        try:
            if frames % round(planets[1].calc_frame_mod()) == 0:
                Planet.match_up_locations(planets[0],planets[1],WIN,frames)
                #print(round(planets[1].calc_frame_mod()))
        except ZeroDivisionError:
            Planet.match_up_locations(planets[0],planets[1],WIN,frames)

        pygame.display.update()

    pygame.quit()


def main():
    planets: List[Planet] = get_planets()
    #task1(planets)
    #task2(planets)
    task3()
    #task4(planets)
    
    #task5()
    # task6()


if __name__ == '__main__':
    main()
    #Planet.match_up_locations(planets[0],planets[1])

    