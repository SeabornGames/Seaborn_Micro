from seaborn_neopixel import SeabornNeoPixel, randint


def main(count=297, segments=10, pin=5, update_rate=0.05, backup_pin=6):
    np = SeabornNeoPixel(count=count, pin=pin, update_rate=update_rate,
                         mock_run_count=20, backup_pin=backup_pin)
    base_colors = ['GREEN', 'RED', 'BLUE', 'YELLOW', 'PURPLE', 'AQUA']
    base_powers = [ 1, 0.5]
    colors = []
    for color in base_colors:
        for p in base_powers:
            colors += np.get_colors(color, power=p)

    iteration = 0
    while np.running:
        iteration += 1
        for i in range(count):
            np[i] = colors[0]
        np.write()
        if True or iteration % 10 == 2:
            rainbow_grow(np, colors, skip=len(base_powers))
            rainbow_shrink(np, colors, skip=len(base_powers))
        return
        continue

        colors.append(colors.pop(0))
        up_index = [round(count / segments * (i + 0.5))
                    for i in range(segments)]
        down_index = up_index + []
        repeat = int(round(count / segments / 2))
        peat = repeat // 2
        for j in range(peat):
            grow_shrink(np, up_index, color[0], 1)
            grow_shrink(np, down_index, color[0], -1)
            np.write()

        if iteration % 5 == 1:
            direction = 1 if iteration % 2 else -1
            for i in range(segments):
                left_right(np, down_index, colors, direction, 0)
                left_right(np, up_index, colors, direction, 1)
                np.write()
            for i in range(segments):
                left_right(np, down_index, colors, -1 * direction, 0)
                left_right(np, up_index, colors, -1 * direction, 1)
                np.write()
        for j in range(peat, repeat):
            grow_shrink(np, up_index, color[0], 1)
            grow_shrink(np, down_index, color[0], -1)
            np.write()


def rainbow_grow(np, colors, skip=1):
    rows = []
    for j in range(len(colors)//skip - 1):
        for i in range(skip):
            colors.append(colors.pop(0))
        rows.append(
            dict(color=colors[0],
                 speed=2 ** len(rows),
                 up=np.count // 2,
                 up_end=np.count,
                 down=np.count // 2,
                 down_end=0))
        for i in range(round(np.count / (4 * rows[-1]['speed']))):
            rainbow_update(np, rows)

    for i in range(rows[0]['down']):
        rainbow_update(np, rows)
    for i in range(np.count):
        np[i] = colors[0]
    np.write()


def rainbow_shrink(np, colors, skip):
    rows = []
    for j in range(len(colors)//skip - 1):
        for i in range(skip):
            colors.append(colors.pop(0))
        rows.append(
            dict(color=colors[0],
                 speed=2 ** (len(colors)//skip - 2 - len(rows)),
                 up=0,
                 up_end=np.count // 2,
                 down=np.count,
                 down_end=np.count // 2))
    for i in range(np.count // 2):
        rainbow_update(np, rows)
    for i in range(np.count):
        np[i] = colors[0]
    np.write()


def rainbow_update(np, rows):
    last_row = None
    for row in rows:
        for ss in range(row['speed']):
            if row['down'] >= row['down_end']:
                np[row['down']] = row['color']
            if last_row is None or last_row['down'] < row['down'] - 2:
                row['down'] -= 1
            if row['up'] <= row['up_end']:
                np[row['up']] = row['color']
            if last_row is None or last_row['up'] > row['up'] + 2:
                row['up'] += 1
        last_row = row
    np.write()


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


def grow_shrink(np, index, color, direction):
    for i in range(len(index)):
        np[index[i]] = color
        index[i] += direction


if __name__ == '__main__':
    keep_running = True
    while keep_running:
        try:
            keep_running = main()
        except Exception as ex:
            print("exception: %s" % ex)
