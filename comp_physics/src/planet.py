from typing import List
import math

import matplotlib.pyplot as plt
import pygame

from src.data import data

WIDTH, HEIGHT = 600,600

class Planet:
    
    AU = 149.6e6 * 1000
    SCALE = 150 / AU
    TIMESTEP = 3600 * 24

    def __init__(self, name, orbital_period, semi_major_axis, mass, eccentricity, inclination,semi_minor_axis,x,y):
        self.name = name
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
    
    def create_orbit(self):
        xcoords = []
        ycoords = []
        time_elapsed = 0
        #a thousand degrees to represent each of the 360
        for i in range (1001):
            distance = (self.semi_major_axis * (1 - self.eccentricity ** 2)) / (1 - self.eccentricity * math.cos(math.radians((9*i)/25)))
            xcoords.append(distance * math.cos(math.radians((9*i)/25)))
            ycoords.append(distance * math.sin(math.radians((9*i)/25)))
            time_elapsed = (((9*i)/25) * self.orbital_period) / (2 * math.pi)
        number_of_seconds = time_elapsed/data['earth_orbit_time']
        print(f'Orbit creation took {number_of_seconds} seconds')
        plt.plot(xcoords, ycoords)

    def create_orbit_z(self):
        xcoords = []
        ycoords = []
        zcoords = []
        for i in range (3601):
            distance = (self.semi_major_axis * (1 - self.eccentricity ** 2)) / (1 - self.eccentricity * math.cos(math.radians(i/10)))
            xcoords.append(distance * math.cos(math.radians(i/10)) * math.cos(math.radians(self.inclination)))
            ycoords.append(distance * math.sin(math.radians(i/10)))
            zcoords.append(distance * math.cos(math.radians(i/10)) * math.sin(math.radians(self.inclination)))
        plt.plot(xcoords, ycoords, zcoords)


def find_semi_minor_axis(idx: int) -> float:
    return data['semi_major_axis'][idx]*((1-(data['eccentricity'][idx]**2)))**0.5


def get_planets() -> List[Planet]:
    """Calculates the semi-minor axis of each planet and returns a list of Planet objects."""

    planet_names: List[str] = ['Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune','Pluto']
    
    planets: List[Planet] = []
    for idx, name in enumerate(planet_names):
        planet = Planet(
            name,
            data['orbital_periods'][idx],
            data['semi_major_axis'][idx],
            data['masses'][idx],
            data['eccentricity'][idx],
            data['inclination'][idx],
            find_semi_minor_axis(idx),
            data['semi_major_axis'][idx] * Planet.AU, 0
        )
        planets.append(planet)
    return planets
