from seaborn_neopixel import SeabornNeoPixel


def main(count=500, step=10, pin=5, update_rate=0.05):
    colors = ['RED', 'GREEN', 'BLUE']
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)
    for i in range(0, count, step):
        for s in range(step):
            np[i+s].set(colors[i%3])
        np.write()
        np.sleep()


if __name__ == '__main__':
    main()
