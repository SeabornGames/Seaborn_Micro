from seaborn_neopixel import SeabornNeoPixel


def main(count=900, pin=5, update_rate=0.005):
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)
    for i in range(count):
        np[i] = 'WHITE'
    np.write()
    colors = np.get_colors('RED', 'GREEN', 'BLUE')
    j = 0
    while np.running:
        j += 1
        color = colors[j % 3]
        for i in range(count - 1, -1, -1) if j % 2 else range(count):
            np[i] = color
            np.write()
            np.sleep()


if __name__ == '__main__':
    main()
