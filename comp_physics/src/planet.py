from typing import List
import math
from random import randint as rand

import matplotlib.pyplot as plt
import pygame

from .data import data

WIDTH, HEIGHT = 700, 700

class Planet:
    
    AU = 149.6e6 * 1000
    SCALE = 10 / AU
    TIMESTEP = 3600 * 24

    def __init__(
        self,
        name,
        orbital_period,
        semi_major_axis,
        mass,
        eccentricity,
        inclination,
        semi_minor_axis,
        color,
        first_four_planets = True
    ):
        self.name = name
        self.orbital_period = orbital_period
        self.semi_major_axis = semi_major_axis
        self.mass = mass
        self.eccentricity = eccentricity
        self.inclination = inclination
        self.semi_minor_axis = semi_minor_axis
        self.color = color

        self.orbit = []
        self.first_four_planets = first_four_planets
        self.distance_to_sun = 0

    def findr(self, angle):
        return ((self.semi_major_axis*(1-(self.eccentricity**2)))/(1-self.eccentricity * math.cos(math.radians(angle))))

    def centre(self):
        return (Planet.findr(self,0)-Planet.findr(self,180))/2

    def DRAW(self, win, location):
        pygame.draw.circle(
            win,
            self.color,
            location,
            10.0
        )

    def get_frames(self):
        if self.first_four_planets:
            number_of_frames = ((360 * self.orbital_period) / (2 * math.pi) / data['earth_orbit_time']) * 60
        else:
            number_of_frames = ((360 * self.orbital_period) / (2 * math.pi) / data['jupiter_orbit_time']) * 60
        indexes_of_together_coords = round(1000/number_of_frames)
        return indexes_of_together_coords
    
    def get_number_of_frames(self, t):
        return ((360 * self.orbital_period) / (2 * math.pi) / t) * 60
    
    def ten_rotations_frames(self):
        t = data['earth_orbit_time'] if self.first_four_planets else data['jupiter_orbit_time']
        return  self.get_number_of_frames(t) * 10

    def create_orbit(self, N=1000):
        xcoords = []
        ycoords = []
        line_coordinates = []
        locations = []
        time_elapsed = 0
        #a thousand degrees to represent each of the 360
        for i in range (N):
            theta = math.radians((9*i)/25)
            distance = (self.semi_major_axis * (1 - self.eccentricity ** 2)) / (1 - self.eccentricity * math.cos(theta))

            xcoord = distance * math.cos(theta)
            ycoord = distance * math.sin(theta)
            xcoords.append(xcoord)
            ycoords.append(ycoord)

            line_coordinate = (
                (xcoord * Planet.AU) * self.SCALE + WIDTH / 2,
                (ycoord * Planet.AU) * self.SCALE + HEIGHT / 2
            )
            line_coordinates.append(line_coordinate)

            if i % Planet.get_frames(self) == 0:
                locations.append(line_coordinate)

        plt.plot(xcoords, ycoords)
        locations = locations * 60 # so there are enough indexes for the planet to loop

        return line_coordinates, locations 

    def create_orbit_z(self):
        xcoords = []
        ycoords = []
        zcoords = []
        for i in range (1000):
            distance = (self.semi_major_axis * (1 - self.eccentricity ** 2)) / (1 - self.eccentricity * math.cos(math.radians(i*9/25)))
            xcoords.append(distance * math.cos(math.radians(i*9/25)) * math.cos(math.radians(self.inclination)))
            ycoords.append(distance * math.sin(math.radians(i*9/25)))
            zcoords.append(distance * math.cos(math.radians(i*9/25)) * math.sin(math.radians(self.inclination)))
        plt.plot(xcoords, ycoords, zcoords)
    
    def match_up_locations(self, other, win, frame):
        togethercoords_self, locations_self = Planet.create_orbit(self)
        togethercoords_other, locations_other = Planet.create_orbit(other)
        pygame.draw.line(win, (0,0,0), locations_self[frame], locations_other[frame], 1)
        #i += 1    

    def calc_frame_mod(self):
        change_in_time = 10 * self.orbital_period / 1234
        return change_in_time * 60


    def time_at_certain_angles(self):
        def simpsons_integration(tuple):
            d_theta = 1/1000
            lower, upper = tuple

            lower = lower * convert_1000_to_360
            upper = upper * convert_1000_to_360
            #bigger = d_theta / ((1 - self.eccentricity * math.cos(math.radians(upper * convert_1000_to_360))) ** 2)
            #smaller = d_theta / ((1 - self.eccentricity * math.cos(math.radians(0))) ** 2)
            
            N = (upper - lower) / d_theta
            N = int(N)
            answer = 0
            for i in range (0, N + 1):
                y_of_n = d_theta / (1 - self.eccentricity * math.cos(math.radians(lower + i * d_theta))) ** 2
                add = y_of_n
                if i == 0 or i == N:
                    answer += add
                elif i % 2 == 0:
                    answer += add * 2
                else:
                    answer += add * 4
            answer = d_theta / 3 * answer 
            return answer
        
        convert_1000_to_360 = (9/25)
        '''
        first_interval = (0, rand(0,1000))
        second_interval = (first_interval[1], rand(first_interval[1],1000))
        third_interval = (second_interval[1], 1000)
        
        time_first_int = (self.orbital_period * (1 - self.eccentricity ** 2) ** (3/2)) * (1 / (2 * math.pi)) * simpsons_integration(first_interval)
        '''
        answer = simpsons_integration((0,1000)) * self.orbital_period * (1 - self.eccentricity ** 2) ** (3/2) * (1 / (2 * math.pi))

        print(answer)



def find_semi_minor_axis(idx: int) -> float:
    return data['semi_major_axis'][idx]*((1-(data['eccentricity'][idx]**2)))**0.5


def get_planets() -> List[Planet]:
    """Calculates the semi-minor axis of each planet and returns a list of Planet objects."""

    planets: List[Planet] = []
    for idx, name in enumerate(data['names']):
        planet = Planet(
            name,
            data['orbital_periods'][idx],
            data['semi_major_axis'][idx],
            data['masses'][idx],
            data['eccentricity'][idx],
            data['inclination'][idx],
            find_semi_minor_axis(idx),
            data['colours'][idx]
        )
        if idx >= 4:
            planet.SCALE = 6 / planet.AU
            planet.first_four_planets = False
        else:
            planet.SCALE = 220 / planet.AU
        planets.append(planet)
    return planets
