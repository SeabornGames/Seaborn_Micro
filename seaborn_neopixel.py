import math, random, time
random.seed(time.time())


def randint(lower, upper):
    gap = upper - lower
    if gap < 2:
        return lower
    return (random.getrandbits(int(math.log(gap, 2))) % gap) + lower


class SeabornNeoPixel():
    def __init__(self, pin, count, update_rate = 0.1, mock_speed_up=10,
                 skip_header=False):
        self.start = time.time()
        self.count = count
        self.mock_speed_up = 1
        try:
            import machine, neopixel
            self.np = neopixel.NeoPixel(machine.Pin(pin), count)
            self.real_mode = True
        except ImportError:
            self.np = [(0, 0, 0) for i in range(count)]
            self.real_mode = False
            self.mock_speed_up = mock_speed_up
            if skip_header:
                print("Running in Mock Mode")
                print(self.header)

        self.update_rate = update_rate / self.mock_speed_up
        self.pixels = [SeabornPixel(i, self) for i in range(count)]

    @property
    def header(self):
        ret = []
        for i in range(4):
            ret.append(('Seconds:  ' if i == 3 else ' '*10) + ''.join(
                [str(a).rjust(4)[i] for a in range(self.count)]))
        return '\33[33m' + '\n'.join(ret) + '\033[0m'

    def __setitem__(self, key, value):
        self.np[key] = value

    def __getitem__(self, key):
        return self.pixels[key]

    @property
    def time_delta(self):
        delta = (time.time() - self.start)
        return delta * self.mock_speed_up

    def sleep(self, update_rate=None, count=1):
        update_rate = self.update_rate if update_rate is None else update_rate
        time.sleep(update_rate * count)

    def write(self, add_header=False):
        if self.real_mode:
            self.np.write()
        else:
            if add_header:
                print(self.header)
            delta = str(round(self.time_delta, 1))
            if '.' not in delta:
                delta += '.0'
            delta = '\33[33m'+ delta.rjust(8) + '  ' + '\033[0m'
            print(delta + ''.join([p.color_char for p in self.pixels]))

    def get_random_pixels(self, count=1, deprioritized_pixels=None):
        ret = []
        unselected_pixels = [p for p in self.pixels
                             if p not in deprioritized_pixels]
        while len(ret) < count:
            if not unselected_pixels:
                unselected_pixels = deprioritized_pixels + []
            i = randint(0, len(unselected_pixels) - 1)
            ret.append(unselected_pixels.pop(i))
        return ret

    def __len__(self):
        return self.count

    def __iter__(self):
        return self.pixels.__iter__()

    def set_all(self, color):
        for p in self.pixels:
            p.set(color)

    def blink(self, count=1, pixels=None, update_rate=None):
        if update_rate is None:
            update_rate = self.update_rate

        if pixels is None:
            pixels = [p for p in self.pixels if p.color != [0, 0, 0]]
        for c in range(count):
            self.write()
            time.sleep(update_rate)
            for a in pixels:
                a.set('BLACK')
            self.write()
            time.sleep(update_rate)
            for a in pixels:
                a.set(a.last_color)

    def fade(self, pixels=None, value=10, count=1):
        pixels = self.pixels if pixels is None else pixels
        for c in range(count):
            for p in pixels:
                p.fade(value)
            self.write()


class SeabornPixel():
    COLORS = {'RED': (255, 0, 0),
              'GREEN': (0, 255, 0),
              'BLUE': (0, 0, 255),
              'WHITE': (255, 255, 255),
              'BLACK': (0, 0, 0),
              'YELLOW': (255,255,0),
              'PURPLE': (160,32,240)}

    def __init__(self, index, seaborn_neopixel):
        self.index = index
        self.seaborn_neopixel = seaborn_neopixel
        self.color = [0, 0, 0]
        self.last_color = [0, 0, 0]

    def set(self, color):
        if isinstance(color, str):
            color = self.COLORS[color]
        self.last_color = self.color
        self.color = list(color)
        if self.color != self.last_color:
            self.seaborn_neopixel[self.index] = tuple(color)

    def fade(self, value=10):
        # XXX this needs to be updated for mixed colors
        self.set([c - value if c > value else 0 for c in self.color])
        return self.color == [0, 0, 0]

    @property
    def color_char(self):
        if self.color[0] == 0 and self.color[1] == 0:
            c = '\33[34m'  # blue
            power = self.color[2]
        elif self.color[0] == 0 and self.color[2] == 0:
            c = '\33[32m'  # green
            power = self.color[1]
        elif self.color[1] == 0 and self.color[2] == 0:
            c = '\33[31m'  # red
            power = self.color[0]
        else:
            c = '\33[37m'  # white
            power = sum(self.color) / 3
        if power == 0:
            return ' '

        SYMBOLS = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        return c + SYMBOLS[int(power // 32)] + '\033[0m'


def main():
    np = SeabornNeoPixel(pin=5, count=50)
    for color in SeabornPixel.COLORS:
        np.set_all(color)
        np.blink()
    np.fade(value=26, count=10)


if __name__ == '__main__':
    main()
