from seaborn_neopixel import SeabornNeoPixel, randint


def main(count=900, number_of_indexes=10, pin=5, update_rate=0.005):
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)
    for i in range(count):
        np[i] = (255, 255, 255)
    np.write()
    np.sleep(count-20)
    np.blink(count=10, color='WHITE')
    colors = np.get_colors('GREEN', 'RED', 'BLUE') #  'YELLOW', 'PURPLE'
    number_of_indexes = number_of_indexes or len(colors)
    indexes = [int(count * i / number_of_indexes)
               for i in range(number_of_indexes)]
    directions =[-1 if randint(0, 100) < 50 else 1] * number_of_indexes
    index_colors =[colors[n % len(colors)] for n in range(number_of_indexes)]
    while np.running:
        for c in range(count):
            for n in range(number_of_indexes):
                np[indexes[n]] = index_colors[n]
                if indexes[n] == count -1 and directions[n] == 1:
                    directions[n] = -1
                elif indexes[n] == 0 and directions[n] == -1:
                    directions[n] = 1
                indexes[n] += directions[n]
            np.write()
            np.sleep()


if __name__ == '__main__':
    main()
