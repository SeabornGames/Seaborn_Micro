from seaborn_neopixel import SeabornNeoPixel


def main(count=200):
    np = SeabornNeoPixel(5, count)
    colors = ['RED', 'GREEN', 'BLUE', 'WHITE']
    for i in range(np.count):
        np[i].set(colors[i%len(colors)])
        np.write()


if __name__ == '__main__':
    main()
