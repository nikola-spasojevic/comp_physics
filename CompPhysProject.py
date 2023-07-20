import math
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pygame
pygame.init()

WIDTH, HEIGHT = 600,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))


data = {
    'G': 6.67 * (10 ** -11),
    'mass_sun': 1.9891 * (10 ** 30),
    'masses':[0.055,0.815,1.00,0.107,317.85,95.16,14.50,17.20,0.00],
    'semi_major_axis': [0.3871,0.7233,1,1.5273,5.2028,9.5388,19.1914,30.0611,39.5294],
    'eccentricity':[0.21,0.01,0.02,0.09,0.05,0.06,0.05,0.01,0.25],
    'inclination':[7.00,3.39,0.00,1.85,1.31,2.49,0.77,1.77,17.5],
    'orbital_periods': [0.2408, 0.6152, 1.0, 1.8809, 11.862, 29.458, 84.01, 164.79, 248.54],
    'earth_orbit_time':57.29577951308232
}

def find_semi_minor_axis(idx):
    return data['semi_major_axis'][idx]*((1-(data['eccentricity'][idx]**2)))**0.5

class Planet:
    
    AU = 149.6e6 * 1000
    SCALE = 150 / AU
    TIMESTEP = 3600 * 24

    def __init__(self, orbital_period, semi_major_axis, mass, eccentricity, inclination,semi_minor_axis,x,y):
        self.orbital_period = orbital_period
        self.semi_major_axis = semi_major_axis
        self.mass = mass
        self.eccentricity = eccentricity
        self.inclination = inclination
        self.semi_minor_axis = semi_minor_axis
        self.color = (255,0,0)
        self.orbit = []

        self.x = x
        self.y = y
        self.distance_to_sun = 0
        self.y_vel = 0
        self.x_vel = 0

    def DRAW(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (x,y), 3.0)

Mercury = Planet(data['orbital_periods'][0], (data['semi_major_axis'][0]),data['masses'][0],data['eccentricity'][0],data['inclination'][0],find_semi_minor_axis(0),data['semi_major_axis'][0] * Planet.AU, 0)
Venus = Planet(data['orbital_periods'][1], (data['semi_major_axis'][1]),data['masses'][1],data['eccentricity'][1],data['inclination'][1],find_semi_minor_axis(1),data['semi_major_axis'][1] * Planet.AU, 0)
Earth = Planet(data['orbital_periods'][2], (data['semi_major_axis'][2]),data['masses'][2],data['eccentricity'][2],data['inclination'][2],find_semi_minor_axis(2),data['semi_major_axis'][2] * Planet.AU, 0)
Mars = Planet(data['orbital_periods'][3], (data['semi_major_axis'][3]),data['masses'][3],data['eccentricity'][3],data['inclination'][3],find_semi_minor_axis(3),data['semi_major_axis'][3] * Planet.AU, 0)
Jupiter = Planet(data['orbital_periods'][4], (data['semi_major_axis'][4]),data['masses'][4],data['eccentricity'][4],data['inclination'][4],find_semi_minor_axis(4),data['semi_major_axis'][4] * Planet.AU, 0)
Saturn = Planet(data['orbital_periods'][5], (data['semi_major_axis'][5]),data['masses'][5],data['eccentricity'][5],data['inclination'][5],find_semi_minor_axis(5),data['semi_major_axis'][5] * Planet.AU, 0)
Uranus = Planet(data['orbital_periods'][6], (data['semi_major_axis'][6]),data['masses'][6],data['eccentricity'][6],data['inclination'][6],find_semi_minor_axis(6),data['semi_major_axis'][6] * Planet.AU, 0)
Neptune = Planet(data['orbital_periods'][7], (data['semi_major_axis'][7]),data['masses'][7],data['eccentricity'][7],data['inclination'][7],find_semi_minor_axis(7),data['semi_major_axis'][7] * Planet.AU, 0)
Pluto = Planet(data['orbital_periods'][8], (data['semi_major_axis'][8]),data['masses'][8],data['eccentricity'][8],data['inclination'][8],find_semi_minor_axis(8),data['semi_major_axis'][8] * Planet.AU, 0)

def task2():
    def create_orbit(planet):
        xcoords = []
        ycoords = []
        time_elapsed = 0
        #a thousand degrees to represent each of the 360
        for i in range (1001):
            distance = (planet.semi_major_axis * (1 - planet.eccentricity ** 2)) / (1 - planet.eccentricity * math.cos(math.radians((9*i)/25)))
            xcoords.append(distance * math.cos(math.radians((9*i)/25)))
            ycoords.append(distance * math.sin(math.radians((9*i)/25)))
            time_elapsed = (((9*i)/25) * planet.orbital_period) / (2 * math.pi)
        number_of_seconds = time_elapsed/data['earth_orbit_time']
        print(number_of_seconds)
        plt.plot(xcoords,ycoords)


    create_orbit(Mercury)
    plt.show()

def task4():
    plt.axes(projection='3d')
    def create_orbit(planet):
        xcoords = []
        ycoords = []
        zcoords = []
        for i in range (3601):
            distance = (planet.semi_major_axis * (1 - planet.eccentricity ** 2)) / (1 - planet.eccentricity * math.cos(math.radians(i/10)))
            xcoords.append(distance * math.cos(math.radians(i/10)) * math.cos(math.radians(planet.inclination)))
            ycoords.append(distance * math.sin(math.radians(i/10)))
            zcoords.append(distance * math.cos(math.radians(i/10)) * math.sin(math.radians(planet.inclination)))

        plt.plot(xcoords,ycoords,zcoords)

    create_orbit(Jupiter)
    create_orbit(Saturn)
    create_orbit(Neptune)
    create_orbit(Uranus)
    create_orbit(Pluto)
    plt.show()


def main():
    run = True
    clock = pygame.time.Clock()


    planets_list = [Mercury]
    other = [Venus, Earth, Mars,Jupiter, Saturn, Uranus, Neptune, Pluto]

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets_list:
            planet.DRAW(WIN)

        pygame.display.update()
    pygame.quit()

#task2()
#task4()
main()
