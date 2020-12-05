from seaborn_neopixel import SeabornNeoPixel


def main(pin=5, update_rate=0.05):
    indexes = [(5, 0, 25, 29),
               (6, 1, 24, 28),
               (7, 2, 23, 27),
               (8, 3, 22, 26),
               (9, 4, 21,),
               (10, 20),
               (11, 19),
               (12, 18),
               (13, 17),
               (14, 16),
               (15,)]
    np = SeabornNeoPixel(pin=pin, count=30, update_rate=update_rate)
    colors = np.get_colors('RED', 'GREEN', 'BLUE', 'YELLOW', 'PURPLE')
    colors += np.get_colors('BLUE', 'RED', 'PURPLE', 'GREEN', 'YELLOW')
    _len = len(indexes)
    current = [[0, 0, 0] for i in range(_len)]
    while np.running:
        for color in colors:
            delta = [(color[0] - current[0][0]) / _len,
                     (color[1] - current[0][1]) / _len,
                     (color[2] - current[0][2]) / _len]
            for i in range(_len * 2):
                cols = [j for j in range(max(0, i - _len), min(_len, i))]
                for c in cols:
                    current[c] = [current[c][0] + delta[0],
                                  current[c][1] + delta[1],
                                  current[c][2] + delta[2]]
                    new_color = (int(current[c][0]),
                                 int(current[c][1]),
                                 int(current[c][2]))
                    for p in indexes[c]:
                        np[p] = new_color
                np.write()
                np.sleep()
            percent = 0.05
            delta = [int(c * percent) for c in color]
            faded_color = np.fade(color, delta=delta, count=4)
            np.fade(faded_color, delta=[-1 * d for d in delta], count=4)


if __name__ == '__main__':
    main()
