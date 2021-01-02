from seaborn_neopixel import SeabornNeoPixel


CRAWL1 = list(range(0,16))
CRAWL2 = list(range(32-1, 16-1, -1))
CRAWL3 = list(range(32,48))
CRAWL4 = list(range(64-1, 48-1, -1))
CRAWL = []
for c in zip(CRAWL2, CRAWL3, CRAWL4, CRAWL1):
    CRAWL += list(c)

WALK1 = list(range(64,80))
WALK2 = list(range(96-1, 80-1, -1))
WALK3 = list(range(96,112))
WALK4 = list(range(128-1, 112-1, -1))
WALK = []
for c in zip(WALK2, WALK3, WALK4, WALK1):
    WALK += list(c)

RUN1 = list(range(128, 144))
RUN2 = list(range(160-1, 144-1, -1))
RUN3 = list(range(160,176))
RUN4 = list(range(192-1, 176-1, -1))
RUN = []
for c in zip(RUN2, RUN3, RUN4, RUN1):
    RUN += list(c)

FLY1 = list(range(192,208))
FLY2 = list(range(224-1, 208-1, -1))
FLY3 = list(range(224,240))
FLY4 = list(range(256-1, 240-1, -1))
FLY = []
for c in zip(FLY2, FLY3, FLY4, FLY1):
    FLY += list(c)



DELAY = [1, 1, 1, 1, 1]


def main(count=256, pin=5, fade_count=10, update_rate=0.005):
    count = len(CRAWL) + len(WALK) + len(RUN) + len(FLY)
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)    
    colors = [np.get_colors('RED', 'ORANGE', 'YELLOW', (200, 128, 64),
                            power=(f/fade_count)/4)
              for f in range(0, fade_count+1)] # [powers][color]
    words = [CRAWL, WALK, RUN, FLY]

    while np.running:
        for i in range(count):
            np[i] = 'BLACK'
        np.write()
        for color, word in enumerate(words):
            index_power = []
            for k, index in enumerate(word + [-1]*fade_count):
                index_power.insert(0, index)
                if len(index_power) > len(colors):
                    index_power.pop(-1)
                for power, _index in enumerate(index_power):
                    np[_index] = colors[power][color]
                if k%2 == 0:
                    np.write()
            np.sleep(DELAY[color])

        for power in range(len(colors) -1, -1, -1):
            for color, word in enumerate(words):
                for index in word:
                    np[index] = colors[power][color]
            np.write()
        np.sleep(DELAY[-1])


if __name__ == '__main__':
    try:
        from micro_secrets import SIZE, PIN
    except:
        SIZE, PIN = 256, 5
    keep_running = True
    while keep_running:
        # try:
        keep_running = main(SIZE, PIN)
        # except Exception as ex:
        #     print("exception: %s" % ex)

