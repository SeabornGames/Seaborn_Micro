from seaborn_neopixel import SeabornNeoPixel

BLACK = (0, 0, 0)


def main(count, pin, update_rate=.1, redirects=None):
    np = SeabornNeoPixel(count=count, pin=pin, update_rate=update_rate,
                         mock_run_count=20, redirects=redirects)
    colors = [(255, 20, 20), 'RED']
    while np.running:
        kiss(np, colors)
        for i in range(3):
            dance(np=np,
                  colors=colors,
                  people_size=2,
                  empty=4)


def kiss(np, colors):
    for i in range(np.count):
        np[i] = 'BLACK'
    np.write()
    _colors = [(20, 20, 20), (32, 0, 0)]
    half_count = (np.count if np.count% 2 == 0 else (np.count + 1)) // 2
    speed = 20
    for i in range(half_count):
        np[i] = _colors[0]
        np[half_count*2 - i] = _colors[1]
        if i % speed == 0:
            np.write()
            speed -= 1 if speed != 1 else 0
    np.write()
    for i in range(half_count):
        np[half_count - i] = 'BLACK'
        np[half_count + i] = 'BLACK'
        for k in range(i):
            np[half_count-i -k -1] = colors[0]
            np[half_count+i +k + 1] = colors[1]
        if i % 3 == 0:
            np.write()
    np.write()


def dance_steps(offsets, middles, **kwargs):
    for offset, middle in zip(offsets, middles):
        dance_step(offset, middle, **kwargs)


def dance_step(offset, middle, np, colors, people_size, empty):
    segment = empty * 2 + people_size * 2 + middle
    for o in range(abs(offset)):
        np[o if offset > 0 else (np.count - 1 - o)] = BLACK
    for i in range(np.count // segment):
        mark = i * segment + offset
        for j in range(empty):
            np[mark + j] = BLACK
        for p in range(people_size):
            np[mark + empty + p] = colors[0]
        for m in range(middle):
            np[mark + empty + people_size + m] = BLACK
        for p in range(people_size):
            np[mark + empty + people_size + middle + p] = colors[1]
        for j in range(empty):
            np[mark + empty + people_size * 2 + j + middle] = BLACK
    np.write()


def dance_spin(offset, np, colors, people_size, empty):
    segment = empty * 2 + people_size * 2
    colors.append(colors.pop(0))
    for p in range(people_size):  # -1, -1, -1):
        for i in range(np.count // segment):
            for c in [0, 1]:
                np[i * segment + empty + c * people_size + p + offset] = colors[
                    c]
        np.write()


def dance(**kwargs):
    dance_steps(offsets=[0, 1, 2, 3],
                middles=[0, 1, 1, 0], **kwargs)
    dance_spin(3, **kwargs)
    dance_steps(offsets=[2, 1, 0, -1, -2, -3],
                middles=[0, 1, 1, 1, 0], **kwargs)
    dance_spin(-3, **kwargs)
    dance_steps(offsets=[-2, -1, 0, 1, 2, 3, 4, 5],
                middles=[0, 1, 1, 0, 0, 1, 1, 0], **kwargs)
    dance_spin(5, **kwargs)
    dance_steps(offsets=[4, 3, 2, 1, 0, -1, -2],
                middles=[1, 1, 0, 0, 1, 1, 0, 0], **kwargs)
    dance_spin(-2, **kwargs)
    dance_steps(offsets=[-1, 0],
                middles=[1, 0, 1, 0], **kwargs)
    for i in range(5):
        dance_spin(0, **kwargs)


if __name__ == '__main__':
    try:
        import micro_secrets
    except:
        micro_secrets = None
    keep_running = True
    while keep_running:
        try:
            keep_running = main(
                count=getattr(micro_secrets, 'SIZE', 300),
                pin=getattr(micro_secrets, 'PIN', 5),
                redirects=getattr(micro_secrets, 'REDIRECT', None))
        except Exception as ex:
            print("exception: %s" % ex)
