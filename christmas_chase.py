from seaborn_neopixel import SeabornNeoPixel


def main(count=110, pin=5, update_rate=0.005):
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)
    while True:
        for i in range(count):
            for c in range(0, count+5, 6):
                np[(c+i+0)%count] = (255, 0, 0)
                np[(c+i+1)%count] = (255, 0, 0)
                np[(c+i+2)%count] = (0, 0, 0)
                np[(c+i+3)%count] = (0, 255, 0)
                np[(c+i+4)%count] = (0, 255, 0)
                np[(c+i+5)%count] = (0, 0, 0)
            n = i + 3
            np[(n+0)%count] = (0, 0, 32)
            np[(n+3)%count] = (0, 0, 64)
            np[(n+6)%count] = (0, 0, 128)
            np[(n+9)%count] = (0, 0, 255)
            np.write()
            np.sleep()


if __name__ == '__main__':
    main()
