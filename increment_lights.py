from seaborn_neopixel import SeabornNeoPixel, SeabornPixel
COLORS = ['RED', 'GREEN', 'BLUE']


def main(start=0, end=100, step=10, update_rate=0.1):
    for i in range(start, end-step, step):
        np = SeabornNeoPixel(pin=5, count=i+step, update_rate=update_rate)
        for j in range(start, i, step):
            for k in range(step):
                np[j+k].set(COLORS[j%3])
        np.write()
        np.sleep()


if __name__ == '__main__':
    main()
