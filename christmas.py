from seaborn_neopixel import SeabornNeoPixel


def main(count, pin, segments=10, update_rate=0.05, redirects=None):
    np = SeabornNeoPixel(count=count, pin=pin, update_rate=update_rate,
                         mock_run_count=20, redirects=redirects)
    base_colors = ['GREEN', 'RED']
    base_powers = [0.75]
    colors = []
    for color in base_colors:
        for p in base_powers:
            colors += np.get_colors(color, power=p)

    iteration = 0
    while np.running:
        iteration += 1
        for i in range(np.count):
            np[i] = colors[0]
        np.write()
        if iteration % 20 == 3:
            rainbow_grow(np)
            rainbow_shrink(np)

        colors.append(colors.pop(0))
        up_index = [round(count / segments * (i + 0.5))
                    for i in range(segments)]
        down_index = up_index + []
        repeat = int(round(count / segments / 2))
        peat = repeat // 2
        for j in range(peat):
            grow_shrink(np, up_index, colors[0], 1)
            grow_shrink(np, down_index, colors[0], -1)
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
            grow_shrink(np, up_index, colors[0], 1)
            grow_shrink(np, down_index, colors[0], -1)
            np.write()


def rainbow_grow(np, colors=None, end_color=None):
    if colors is None:
        colors = np.get_colors('PURPLE', 'GREEN', 'RED' , 'BLUE', 'YELLOW',
                               'AQUA', 'WHITE', power=.50)
    if end_color is None:
        end_color = colors[0]
    rows = []
    for j in range(len(colors)):
        colors.append(colors.pop(0))
        rows.append(
            dict(color=colors[0],
                 speed=2 ** len(rows) + int(round(np.roll_count / 300) - 1),
                 up=np.roll_count // 2,
                 up_end=np.roll_count,
                 down=np.roll_count // 2,
                 down_end=0))
        for i in range(round(np.roll_count / (4 * rows[-1]['speed']))):
            rainbow_update(np, rows)

    for i in range(rows[0]['down']):
        rainbow_update(np, rows)
    for i in range(np.roll_count):
        np[i] = colors[0]
    np.write()

    if end_color != colors[0]:
        np.fade(colors[0])


def rainbow_shrink(np, colors):
    rows = []
    for j in range(len(colors)):
        colors.append(colors.pop(0))
        rows.append(
            dict(color=colors[0],
                 speed=2 ** (len(colors) - 1 - len(rows)),
                 up=0,
                 up_end=np.roll_count // 2,
                 down=np.roll_count,
                 down_end=np.roll_count // 2))
    for i in range(np.roll_count // 2):
        rainbow_update(np, rows)
    for i in range(np.roll_count):
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
        np[np.roll_count - 1] = colors[0]
    for i in range(len(index)):
        np[index[i]] = colors[c]
        index[i] += direction


def grow_shrink(np, index, color, direction):
    for i in range(len(index)):
        np[index[i]] = color
        index[i] += direction


if __name__ == '__main__':
    try:
        import micro_secrets
    except:
        micro_secrets = None
    keep_running = True
    while keep_running:
        try:
            keep_running = main(
                size = getattr(micro_secrets, 'SIZE', 300),
                pin = getattr(micro_secrets, 'PIN', 5),
                inverse = getattr(micro_secrets, 'INVERSE', False),
                redirect = getattr(micro_secrets, 'REDIRECT', None))
        except Exception as ex:
            print("exception: %s" % ex)
