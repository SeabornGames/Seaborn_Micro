from seaborn_neopixel import SeabornNeoPixel, SeabornPixel
COLORS = ['RED', 'GREEN', 'BLUE']


def main(start=0, end=500, step=10, update_rate=0.1):
    np = None
    for i in range(start, end, step):
        # if np is not None:
        #     np.fade(value=26, count=10)
        np = SeabornNeoPixel(pin=5, count=i+step, update_rate=update_rate,
                             skip_header=i)
        for j in range(start, i+step, step):
            for k in range(step):
                np[j+k].set(COLORS[j%3])
        np.write()


if __name__ == '__main__':
    main()
