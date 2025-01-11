#!/usr/bin/env python3

import curses
import random
import math

# Constants for simulation
G = 6.67430e-11  # Gravitational constant (real-world value, adjust as necessary for visibility)
DT = 0.01        # Time step for simulation
NUM_BODIES = 3   # Number of bodies in the simulation
WIDTH = 80       # Width of the ASCII display
HEIGHT = 24      # Height of the ASCII display

class Body:
    def __init__(self):
        # Initialize position randomly within a central area of the screen
        self.x = random.uniform(WIDTH * 0.3, WIDTH * 0.7)
        self.y = random.uniform(HEIGHT * 0.3, HEIGHT * 0.7)
        # Initialize previous positions for Verlet integration
        self.px = self.x - random.uniform(-1.0, 1.0)  
        self.py = self.y - random.uniform(-1.0, 1.0)  
        # Random mass for each body
        self.mass = random.uniform(1.0, 4.0)

def update_positions(bodies):
    # Calculate forces and update positions using Verlet integration
    for i in range(NUM_BODIES):
        fx, fy = 0.0, 0.0
        for j in range(NUM_BODIES):
            if i != j:
                dx = bodies[j].x - bodies[i].x
                dy = bodies[j].y - bodies[i].y
                dist_sqr = dx*dx + dy*dy + 1e-9  # Small epsilon to avoid division by zero
                force = G * bodies[i].mass * bodies[j].mass / dist_sqr
                fx += force * dx / math.sqrt(dist_sqr)
                fy += force * dy / math.sqrt(dist_sqr)

        # Verlet integration
        new_x = 2 * bodies[i].x - bodies[i].px + (fx / bodies[i].mass) * DT * DT
        new_y = 2 * bodies[i].y - bodies[i].py + (fy / bodies[i].mass) * DT * DT
        bodies[i].px, bodies[i].py = bodies[i].x, bodies[i].y
        bodies[i].x, bodies[i].y = new_x, new_y

        # Screen wrapping to keep all bodies within view
        bodies[i].x %= WIDTH
        bodies[i].y %= HEIGHT

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Don't block I/O calls
    stdscr.timeout(50)  # Set screen refresh rate

    bodies = [Body() for _ in range(NUM_BODIES)]

    while True:
        stdscr.erase()  # Clear the screen for new drawing

        update_positions(bodies)

        # Draw the bodies
        for body in bodies:
            stdscr.addch(int(body.y) % HEIGHT, int(body.x) % WIDTH, '*')

        stdscr.refresh()  # Refresh the screen to show updates

        if stdscr.getch() != -1:  # Exit on any key press
            break

if __name__ == '__main__':
    curses.wrapper(main)
