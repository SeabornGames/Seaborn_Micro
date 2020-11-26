from seaborn_neopixel import SeabornNeoPixel, SeabornPixel
COLORS = ['RED', 'GREEN', 'BLUE']


def main(count=1200, update_rate=0.02):
    np=None
    for i in range(1, count):
        np = SeabornNeoPixel(pin=5, count=count, update_rate=update_rate)
        for j in range(len(np)):
            np.fade()
            np[j].set(COLORS[i%3])
            np.write()
            np.sleep()
        np.fade(count=26)
    np.set_all('WHITE')


if __name__ == '__main__':
    main()
