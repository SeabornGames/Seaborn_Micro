from seaborn_neopixel import SeabornNeoPixel


def main(count=32, pin=5, update_rate=0.005):
    np = SeabornNeoPixel(pin=pin, count=count, update_rate=update_rate)
    for i in range(count):
        np[i] = 'BLUE'
    np.write()
    colors = np.get_colors('RED', 'GREEN', 'BLUE', 'PURPLE', 
        'YELLOW', 'AQUA', power=.5)    
    j = 0
    while np.running:
        j += 1
        color = colors[j % len(colors)]
        for i in range(count - 1, -1, -1) if j % 2 else range(count):
            np[i] = color
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

