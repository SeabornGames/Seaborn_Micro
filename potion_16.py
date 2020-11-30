from seaborn_neopixel import SeabornNeoPixel


def main(count=16, pin=5, update_rate=0.5):
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)
    colors = np.get_colors('RED', 'GREEN', 'BLUE', 'YELLOW')
    quadrents = {0: [0, 1, 4, 5],
                 1: [2, 3, 6, 7],
                 2: [10, 11, 14, 15],
                 3: [8, 9, 12, 13]}
    while True:
        for c in range(4):
            for i in range(4):
                for j in quadrents[i]:
                    np[j] = colors[(c+i) % 4]
            np.write()
            np.sleep()


if __name__ == '__main__':
    main()
