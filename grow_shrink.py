from seaborn_neopixel import SeabornNeoPixel, randint


def main(count=297, segments=10, pin=5, update_rate=0.5):
    np = SeabornNeoPixel(count=count, pin=pin, update_rate=update_rate)
    colors = np.get_colors('GREEN', 'RED')

    while np.running:
        for i in range(count):
            np[i] = colors[0]
        np.write()
        np.sleep()
        colors = colors[1:] + colors[:1]
        up_index = [round(count / segments * i) for i in range(segments)]
        down_index = [round(count / segments * i) for i in range(segments)]
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
    while True:
        try:
            main()
        except Exception:
            pass
