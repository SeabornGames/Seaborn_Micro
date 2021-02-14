from seaborn_neopixel import SeabornNeoPixel


def main(count=32, pin=5, step=10, update_rate=0.05):
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)
    colors = np.get_colors('RED', 'GREEN', 'BLUE', 'PURPLE', 
        'YELLOW', 'AQUA')
    for i in range(0, count, step):
        for s in range(step):
            np[i + s] = colors[i % len(colors)]
        np.write()
        np.sleep()


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
