#!/usr/bin/env python3

import curses
import time
import random
import math

# Simulation parameters
G = 1e2        # Gravitational constant (scaled for visible movement)
DT = 0.01      # Time step
NUM_BODIES = 3 # We only have 3 bodies

# The "universe" size in ASCII coordinates
WIDTH = 80
HEIGHT = 24

class Body:
    def __init__(self):
        # Random initial positions in a smaller bounding box
        self.x = random.uniform(WIDTH * 0.3, WIDTH * 0.7)
        self.y = random.uniform(HEIGHT * 0.3, HEIGHT * 0.7)
        # Random initial velocity
        self.vx = random.uniform(-2.0, 2.0)
        self.vy = random.uniform(-2.0, 2.0)
        # All bodies have some arbitrary mass
        self.mass = random.uniform(1.0, 4.0)

def main(stdscr):
    curses.curs_set(0)            # Hide the cursor
    stdscr.nodelay(True)          # Make getch() non-blocking
    stdscr.timeout(50)           # Refresh rate in ms

    # Initialize bodies
    bodies = [Body() for _ in range(NUM_BODIES)]
    
    while True:
        # Clear screen
        stdscr.erase()

        # Calculate gravitational forces & update positions
        for i in range(NUM_BODIES):
            fx, fy = 0.0, 0.0
            for j in range(NUM_BODIES):
                if i == j:
                    continue
                dx = bodies[j].x - bodies[i].x
                dy = bodies[j].y - bodies[i].y
                dist_sqr = dx*dx + dy*dy + 1e-9  # Avoid zero division
                dist = math.sqrt(dist_sqr)
                force = (G * bodies[i].mass * bodies[j].mass) / dist_sqr
                fx += force * dx / dist
                fy += force * dy / dist

            # Euler integration
            bodies[i].vx += (fx / bodies[i].mass) * DT
            bodies[i].vy += (fy / bodies[i].mass) * DT
            bodies[i].x  += bodies[i].vx * DT
            bodies[i].y  += bodies[i].vy * DT

            # Keep bodies within ASCII window (simple wrap-around)
            bodies[i].x %= WIDTH
            bodies[i].y %= HEIGHT

        # Draw bodies
        for b in bodies:
            # Convert float coords to integer within terminal
            bx = int(b.x)
            by = int(b.y)
            if 0 <= bx < WIDTH and 0 <= by < HEIGHT:
                stdscr.addch(by, bx, '*')

        # Refresh the screen
        stdscr.refresh()
        time.sleep(0.05)

        # Check if user pressed any key
        if stdscr.getch() != -1:
            break

if __name__ == '__main__':
    curses.wrapper(main)
