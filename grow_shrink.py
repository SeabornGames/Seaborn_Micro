from seaborn_neopixel import SeabornNeoPixel, randint


def main(count=297, segments=10, pin=5, update_rate=0.05, backup_pin=6):
    np = SeabornNeoPixel(count=count, pin=pin, update_rate=update_rate,
                         mock_run_count=20, backup_pin=backup_pin)
    colors = []
    for color in ['GREEN', 'RED', 'BLUE', 'YELLOW',
                  'PURPLE', 'AQUA', 'WHITE']:
        for p in [0.5, 1]:
            colors += np.get_colors(color, power=p)

    iteration = 0
    while np.running:
        iteration += 1
        for i in range(count):
            np[i] = colors[0]
        np.write()
        np.sleep()
        colors = colors[1:] + colors[:1]
        up_index = [round(count / segments * (i + 0.5))
                    for i in range(segments)]
        down_index = up_index + []
        repeat = int(count / segments / 2)
        peat = repeat // 2
        for j in range(peat):
            grow_shrink(np, up_index, colors, 1)
            grow_shrink(np, down_index, colors, -1)

        if iteration % 5 == 1:
            direction = 1 if iteration % 2 else -1
            for i in range(segments):
                left_right(np, down_index, colors, direction, 0)
                left_right(np, up_index, colors, direction, 1)
            for i in range(segments):
                left_right(np, down_index, colors, -1 * direction, 0)
                left_right(np, up_index, colors, -1 * direction, 1)

        for j in range(peat, repeat):
            grow_shrink(np, up_index, colors, 1)
            grow_shrink(np, down_index, colors, -1)


def left_right(np, index, colors, direction, right):
    if right:
        c = 0 if direction == 1 else -1
    else:
        c = -1 if direction == 1 else 0
    if direction == 1:
        np[0] = colors[-1]
    else:
        np[np.count - 1] = colors[0]
    for i in range(len(index)):
        np[index[i]] = colors[c]
        index[i] += direction
        np[index[i]] = colors[c]
    np.write()
    np.sleep()


def grow_shrink(np, index, colors, direction):
    for i in range(len(index)):
        np[index[i]] = colors[0]
        index[i] += direction
    np.write()
    np.sleep()


if __name__ == '__main__':
    keep_running = True
    while keep_running:
        # try:
        keep_running = main()
        # except Exception as ex:
        #     print("exception: %s" % ex)
