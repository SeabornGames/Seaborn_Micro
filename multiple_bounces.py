from seaborn_neopixel import SeabornNeoPixel, randint


def main(count=900, number_of_indexes=15, pin=5, update_rate=0.005):
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)
    for i in range(count):
        np[i] = (200, 200, 200)
    np.write()
    np.blink(count=10, color='WHITE')
    # colors = np.get_colors('GREEN', 'RED', 'BLUE') #  'YELLOW', 'PURPLE'
    colors = [(200, 0, 0), (0, 200, 0), (0, 0, 200)]
    number_of_indexes = number_of_indexes or len(colors)
    directions =[(randint(-3, 3) or 1) for i in range(number_of_indexes)]
    indexes = [int(count * i / number_of_indexes)
               for i in range(number_of_indexes)]

    index_colors =[colors[n % len(colors)] for n in range(number_of_indexes)]
    while np.running:
        for c in range(count):
            for n in range(number_of_indexes):
                if indexes[n] >= count and directions[n] == 1:
                    directions[n] *= -1
                    indexes[n] = count-1
                elif indexes[n] < 0 and directions[n] == -1:
                    directions[n] *= -1
                    indexes[n] = 0
                if directions[n] > 0:
                    for i in range(directions[n]):
                        np[indexes[n] + i] = index_colors[n]
                else:
                    for i in range(directions[n], 0):
                        np[indexes[n] + i] = index_colors[n]
                indexes[n] += directions[n]
            np.write()


if __name__ == '__main__':
    main()
