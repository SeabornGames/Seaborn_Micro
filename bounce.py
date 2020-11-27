from seaborn_neopixel import SeabornNeoPixel


def main(count=60, pin=5, update_rate=0.005):
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)
    colors = np.get_colors('RED', 'GREEN', 'BLUE')
    for j in range(10000):
        color = colors[j % 3]
        for i in range(count - 1, -1, -1) if j % 2 else range(count):
            np[i] = color
            np.write()
            np.sleep()


if __name__ == '__main__':
    main()
