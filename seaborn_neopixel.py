import math, random, time

random.seed(time.time())


def randint(lower, upper):
    gap = upper - lower
    if gap < 2:
        return lower
    return (random.getrandbits(int(math.log(gap, 2))) % gap) + lower


class SeabornEngine:
    def __init__(self, threads=None):
        self.threads = threads or []

    def __iter__(self):
        while self.threads:
            ret = []
            for i in range(len(self.threads) - 1, -1, -1):
                ret.append(self.threads[i]())
            yield ret

    def append(self, thread):
        self.threads.append(thread)

    def add_transition(self, np, index, colors, steps):
        thread = SeabornTransition(np, index, colors, steps)
        self.threads.append(thread)


class SeabornTransition:
    def __init__(self, np, index, colors, steps):
        self.np = np
        self.index = index
        self.colors = colors
        self.steps = steps
        self.n = -1

    def __call__(self):
        self.n += 1
        c1 = self.colors[0]
        c2 = self.colors[1]
        new_color = (c1[0] - (c1[0] - c2[0]) * self.n // self.steps[0],
                     c1[1] - (c1[1] - c2[1]) * self.n // self.steps[0],
                     c1[2] - (c1[2] - c2[2]) * self.n // self.steps[0])
        self.np[self.index] = new_color
        # print("index: %-5s  color: %15s   %s / %s" % (
        #     self.index, new_color, self.n, self.steps[0]))
        if self.n == self.steps[0] - 1:
            self.n = -1
            self.colors.pop(0)
            self.steps.pop(0)
        return None if bool(self.steps) else self


class SeabornNeoPixel:
    COLORS = {'RED': (255, 0, 0),
              'GREEN': (0, 255, 0),
              'BLUE': (0, 0, 255),
              'WHITE': (255, 255, 255),
              'BLACK': (0, 0, 0),
              'YELLOW': (255, 255, 0),
              'PURPLE': (160, 32, 240)}

    def __init__(self, pin, count, update_rate=0.1, mock_speed_up=10,
                 mock_run_count=1, skip_header=False):
        self.start = time.time()
        self.count = count
        self.mock_speed_up = 1
        try:
            import machine, neopixel
            self.np = neopixel.NeoPixel(machine.Pin(pin), count)
        except ImportError:
            self.run_count = mock_run_count
            self.np = [(0, 0, 0) for i in range(count)]
            self.mock_speed_up = mock_speed_up
            if skip_header:
                print("Running in Mock Mode")
                print(self.header)
        self.update_rate = update_rate / self.mock_speed_up

    @classmethod
    def get_colors(cls, *colors):
        return [cls.COLORS.get(c, c) for c in colors]

    @property
    def header(self):
        ret = []
        for i in range(4):
            ret.append(('Seconds:  ' if i == 3 else ' ' * 10) + ''.join(
                [str(a).rjust(4)[i] for a in range(self.count)]))
        return '\33[33m' + '\n'.join(ret) + '\033[0m'

    def __setitem__(self, index, color):
        if index < 0 or index >= self.count:
            return
        if isinstance(color, str):
            color = self.COLORS[color]
        self.np[index] = color

    @property
    def time_delta(self):
        delta = (time.time() - self.start)
        return delta * self.mock_speed_up

    def sleep(self, update_rate=None, count=1):
        update_rate = self.update_rate if update_rate is None else update_rate
        time.sleep(update_rate * count)

    def write(self, add_header=False):
        if isinstance(self.np, list):  # running in mock mode
            if add_header:
                print(self.header)
            delta = str(round(self.time_delta, 1))
            if '.' not in delta:
                delta += '.0'
            delta = '\33[33m' + delta.rjust(8) + '  ' + '\033[0m'
            print(delta + ''.join([self.color_char(i)
                                   for i in range(self.count)]))
        else:
            self.np.write()

    def get_random_pixel_indexes(self, count=1, deprioritized_pixels=None):
        ret = []
        unselected_pixels = [i for i in range(self.count)
                             if i not in deprioritized_pixels]
        while len(ret) < count:
            if not unselected_pixels:
                unselected_pixels = deprioritized_pixels + []
            i = randint(0, len(unselected_pixels) - 1)
            ret.append(unselected_pixels.pop(i))
        return ret

    @property
    def running(self):
        if isinstance(self.np, list):  # running in mock mode
            self.run_count -= 1
            return self.run_count >= 0
        else:
            return True

    def __len__(self):
        return self.count

    def __iter__(self):
        for i in range(self.count):
            yield self.np[i]

    def set_all(self, color):
        if isinstance(color, str):
            color = self.COLORS[color]
        for i in range(self.count):
            self.np[i] = color

    def blink(self, color, pixel_indexes=None, count=1, update_rate=None):
        update_rate = self.update_rate if update_rate is None else update_rate
        if pixel_indexes is None:
            pixel_indexes = range(self.count)
        if isinstance(color, str):
            color = self.COLORS[color]
        for c in range(count):
            self.write()
            time.sleep(update_rate)
            for i in pixel_indexes:
                self.np[i] = (0, 0, 0)
            self.write()
            time.sleep(update_rate)
            for i in pixel_indexes:
                self.np[i] = color

    def fade(self, color, pixel_indexes=None, count=10, percent=10,
             update_rate=None, delta=None):
        update_rate = self.update_rate if update_rate is None else update_rate
        if pixel_indexes is None:
            pixel_indexes = range(self.count)
        if isinstance(color, str):
            color = self.COLORS[color]
        if delta is None:
            delta = [c // percent + (1 if c % percent else 0) for c in color]
        for c in range(count):
            color = (color[0] - delta[0],
                     color[1] - delta[1],
                     color[2] - delta[2])
            for i in pixel_indexes:
                self.np[i] = color
            self.write()
            time.sleep(update_rate)
        return color

    def color_char(self, index):
        color = self.np[index]
        if color[0] == 0 and color[1] == 0:
            c = '\33[34m'  # blue
            power = color[2]
        elif color[0] == 0 and color[2] == 0:
            c = '\33[32m'  # green
            power = color[1]
        elif color[1] == 0 and color[2] == 0:
            c = '\33[31m'  # red
            power = color[0]
        else:
            c = '\33[37m'  # white
            power = sum(color) / 3
        if power == 0:
            return ' '

        SYMBOLS = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        return c + SYMBOLS[int(power // 32)] + '\033[0m'


def main():
    np = SeabornNeoPixel(pin=5, count=50)
    for color in SeabornNeoPixel.COLORS:
        np.set_all(color)
        np.blink(color)

    for color in SeabornNeoPixel.COLORS:
        np.set_all(color)
        np.fade(color)


if __name__ == '__main__':
    main()
