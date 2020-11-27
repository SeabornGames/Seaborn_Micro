import machine, neopixel, time


def main(count=500, pin=5, update_rate=0.005):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    np = neopixel.NeoPixel(machine.Pin(pin), count)
    for i in range(10):
        for i in range(count):
            np[i] = (0, 0, 0)
        np.write()
        time.sleep(.5)
        for i in range(count):
            np[i] = (255, 255, 255)
        np.write()
        time.sleep(3)

    for j in range(10000):
        color = colors[j % 3]
        for i in range(count - 1, -1, -1) if j % 2 else range(count):
            np[i] = color
            np.write()
            time.sleep(update_rate)


if __name__ == '__main__':
    main()
