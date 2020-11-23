"""
    This runs after boot.py
"""
import machine, neopixel, time


def main():
    np = neopixel.NeoPixel(machine.Pin(5), 50)

    for s in range(10):
        for i in range(50):
            for k in range(50):
                np[k] = (0, 0, 0)
            for j in range(s):
                if 0 <= i - j < 50:
                    np[i-j] = (128+j*5, 256 - s * 20+j*5, s * 40+j*5)
            np.write()
            time.sleep(0.1)


if __name__ == '__main__':
    main()
