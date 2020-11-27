from seaborn_neopixel import SeabornNeoPixel


def main(count=75, pin=5, update_rate=0.1):
    colors = ['RED', 'GREEN', 'BLUE']
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)
    for j in range(10000):
        color = colors[j%3]
        for i in range(count-1, -1, -1) if j%2 else range(count):
            np[i].set(color)
            np.write()
            np.sleep()


if __name__ == '__main__':
    main()
