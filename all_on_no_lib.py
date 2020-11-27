import machine, neopixel, time


def main(count=500, step=50, pin=5, update_time=0.05):
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    np = neopixel.NeoPixel(machine.Pin(pin), count)
    for i in range(0, count, step):
        for s in range(step):
            np[i + s] = colors[i % 3]
        np.write()
        time.sleep(update_time)


if __name__ == '__main__':
    main()
