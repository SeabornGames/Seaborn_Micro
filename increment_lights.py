from seaborn_neopixel import SeabornNeoPixel, SeabornPixel
COLORS = ['RED', 'GREEN', 'BLUE']


def main(start=0, end=1200, step=10, update_rate=0.1):
    for i in range(start, end, step):
        np = SeabornNeoPixel(pin=5, count=i+step, update_rate=update_rate,
                             skip_header=i)
        for j in range(start, i+step, step):
            for k in range(step):
                np[j+k].set(COLORS[j%3])
        np.write()
        np.fade(value=26, count=10)


if __name__ == '__main__':
    main()
