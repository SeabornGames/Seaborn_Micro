from seaborn_neopixel import SeabornNeoPixel, SeabornPixel
from seaborn_esp import connect_to_network, request_rtc, STATUS, setup_status
from micro_secrets import NAME


def main(count=50):
    np = SeabornNeoPixel(pin=5, count=50)
    setup_status(np.pixels[0:1], STATUS.ready, 'setup microchip: %s' % NAME)
    connect_to_network(pixels=np.pixels[1:2])
    request_rtc(pixels=np.pixels[2:3])
    setup_status(np.pixels[0:1], STATUS.go, 'setup complete for: %s' % NAME)
    while True:
        for color in SeabornPixel.COLORS:
            np.set_all(color)
            np.write()
            np.sleep()
            np.fade(count=10)


if __name__ == '__main__':
    main()
