from seaborn_neopixel import SeabornNeoPixel


def main(count=110, pin=5, update_rate=0.005):
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)
    while True:
        for i in range(count):
            for c in range(0, count, 8):
                color = max(255 - c*2, 0)
                np[(c + i + 0) % count] = (color, 0, 0)
                np[(c + i + 1) % count] = (color, 0, 0)
                np[(c + i + 2) % count] = (0, 0, 0)
                np[(c + i + 3) % count] = (0, 0, 0)
                np[(c + i + 4) % count] = (0, color, 0)
                np[(c + i + 5) % count] = (0, color, 0)
                np[(c + i + 6) % count] = (0, 0, 0)
                np[(c + i + 7) % count] = (0, 0, 0)
            n = count - i + 2
            np[(n + 0) % count] = (0, 0, 255)
            np[(n + 1) % count] = (0, 0, 198)
            np[(n + 4) % count] = (0, 0, 128)
            np[(n + 5) % count] = (0, 0, 64)
            np[(n + 8) % count] = (0, 0, 32)
            np[(n + 9) % count] = (0, 0, 16)
            np[(n + 12) % count] = (0, 0, 8)
            np[(n + 13) % count] = (0, 0, 8)
            np.write()
            np.sleep()


if __name__ == '__main__':
    main()
