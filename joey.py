from seaborn_neopixel import SeabornNeoPixel, randint


def main(count=297, segments=10, pin=4, update_rate=0.05, backup_pin=None):
    np = SeabornNeoPixel(count=count, pin=pin, update_rate=update_rate,
                         mock_run_count=89, backup_pin=backup_pin)
    colors = np.get_colors('GREEN', 'RED')
    # colors = [(64, 0, 0), (0, 64, 0)]

    for i in range(count):
        np[i] = colors[0]
    while np.running:
        coinflip = randint(0, len(colors))
        for i in range(count):
            diceroll = randint(0,4)
            if diceroll == 0:
                np[i] = colors[coinflip]

        np.write()
        np.sleep()


if __name__ == '__main__':
    keep_running = True
    while keep_running:
        try:
            keep_running = main()
        except Exception as ex:
            print("exception: %s"%ex)
