from seaborn_neopixel import SeabornNeoPixel, randint


def main(count=297, segments=10, pin=5, update_rate=0.05, backup_pin=6):
    np = SeabornNeoPixel(count=count, pin=pin, update_rate=update_rate,
                         mock_run_count=9, backup_pin=backup_pin)
    colors = np.get_colors('GREEN', 'RED')
    colors = [(128, 0, 0), (0, 128, 0)]


    while np.running:
        for i in range(count):
            np[i] = colors[0]
        np.write()
        np.sleep()
        colors = colors[1:] + colors[:1]
        up_index = [round(count / segments * (i + 0.5))
                    for i in range(segments)]
        down_index = up_index + []
        repeat = int(count / segments / 2)
        for j in range(repeat):
            for i in range(len(up_index)):
                np[up_index[i]] = colors[0]
                up_index[i] += 1
            np.write()
            np.sleep()
            for i in range(len(down_index)):
                np[down_index[i]] = colors[0]
                down_index[i] -= 1
            np.write()
            np.sleep()


if __name__ == '__main__':
    keep_running = True
    while keep_running:
        try:
            keep_running = main()
        except Exception as ex:
            print("exception: %s"%ex)
