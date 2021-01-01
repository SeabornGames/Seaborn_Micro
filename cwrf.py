from seaborn_neopixel import SeabornNeoPixel


CRAWL = [1, 2, 3]
DELAY = [1,1,1,1,1]

def main(count=32, pin=5, update_rate=0.005):
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)
    for i in range(count):
        np[i] = 'BLACK'
    np.write()
    colors = np.get_colors('RED', 'ORANGE', 'YELLOW', 'WHITE', power=1)    
    words = [CRAWL, WALK, RUN, FLY]

    while np.running:
        for i, word in enumerate(words):
            for index in word:
                np[index] = colors[i]
                np.write()
            time.sleep(DELAY[i])
#        np.fade()
#    def fade(self, color, pixel_indexes=None, count=10, percent=10,
#             update_rate=None, delta=None):

if __name__ == '__main__':
    try:
        from micro_secrets import SIZE, PIN
    except:
        SIZE, PIN = 32, 5
    keep_running = True
    while keep_running:
        try:
            keep_running = main(SIZE, PIN)
        except Exception as ex:
            print("exception: %s" % ex)

