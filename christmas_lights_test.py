from seaborn_neopixel import SeabornNeoPixel, SeabornPixel
from seaborn_esp import connect_to_network, request_rtc, STATUS, setup_status
from micro_secrets import NAME


def main(count=1200, skip_setup=False):
    np = SeabornNeoPixel(pin=5, count=count)
    if not skip_setup:
        setup_status(np.pixels[0:1], STATUS.ready, 'setup microchip: %s' % NAME)
        connect_to_network(pixels=np.pixels[1:2])
        np.start = request_rtc(pixels=np.pixels[2:3])
        setup_status(np.pixels[0:1], STATUS.go, 'setup complete for: %s' % NAME)
    while True:
        for color in SeabornPixel.COLORS:
            if color is 'BLACK':
                continue
            np.set_all(color)
            np.write()
            np.sleep()
            np.fade(count=26)


if __name__ == '__main__':
    main()
