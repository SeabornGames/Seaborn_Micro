"""
    This module simulates bullet holes lighting up
"""

import time
from seaborn_neopixel import SeabornNeoPixel

NUM_OF_PIXELS = 49

ORDERS = [(1, 2), (2, 3), (5, 10), (5, 10), (1, 3), (2, 4), (3, 6), (5, 15),
          (2, 6), (3, 9), (5, 15), (NUM_OF_PIXELS, 5)]


def fade_nodes(np, fading_nodes):
    for fading_node in fading_nodes + []:
        if fading_node.fade():
            fading_nodes.remove(fading_node)
    np.write()
    time.sleep(np.update_rate)


def main():
    np = SeabornNeoPixel(pin=5, count=NUM_OF_PIXELS)
    np.set_all('BLUE')
    np.blink(5)
    np.set_all('BLACK')
    fading_nodes = []
    while True:
        for count, seconds in ORDERS:
            nodes = np.get_random_pixels(count, fading_nodes)
            for n in nodes:
                n.set('RED')
                fade_count = int((seconds / np.mock_speed_up) /
                                 (count * np.update_rate))
                for i in range(fade_count):
                    fade_nodes(np, fading_nodes)
                fading_nodes.append(n)
        while fading_nodes:
            fade_nodes(np, fading_nodes)


if __name__ == '__main__':
    main()
