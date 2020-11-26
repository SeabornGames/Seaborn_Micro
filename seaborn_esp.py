"""
    Seaborn wrapper around libraries and script for easy access
"""

import socket
from micro_secrets import ESSID, ESSID_PWD, NAME


class STATUS:
    ready = 'READY'
    set = 'SET'
    go = 'GO'
    problem = 'PROBLEM'
    exception = 'EXCEPTION'


def connect_to_network(pixels=None):
    # sta_if STA mode allows the ESP8266 to connect to a Wi-Fi network
    # ap_if AP mode allows it to create its own network and have other devices

    try:
        import network
    except ImportError:
        return mock_connect_to_network(pixels)
    try:
        setup_status(pixels, STATUS.ready, 'initializing network')
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            sta_if.active(True)
            setup_status(pixels, STATUS.set, 'connecting to network')
            sta_if.connect(ESSID, ESSID_PWD)
            while not sta_if.isconnected():
                setup_status(pixels, STATUS.problem, 'problem connecting')
                if pixels:
                    pixels[0].blink(1, pixels, 0.1)
                pass
        setup_status(pixels, STATUS.go, 'network configured')
    except Exception as ex:
        setup_status(pixels, STATUS.exception, ex)
        raise


def mock_connect_to_network(pixels):
    setup_status(pixels, STATUS.ready, 'initializing network')
    setup_status(pixels, STATUS.set, 'connecting to network')
    setup_status(pixels, STATUS.problem, 'problem connecting')
    setup_status(pixels, STATUS.go, 'network configured')


def setup_status(pixels, status, message, end=None):
    if end is None:
        print("setup_status: %s -- %s"%(status, message))
    else:
        print(message, end=end)

    if not pixels:
        return

    if not isinstance(pixels, list):
        pixels = [pixels]

    color = {STATUS.ready: 'WHITE',
             STATUS.set: 'BLUE',
             STATUS.go: 'GREEN',
             STATUS.problem: 'YELLOW',
             STATUS.exception: 'RED'
             }.get(status, 'PURPLE')

    for p in pixels:
        p.set(color)
    if status in [STATUS.problem, STATUS.go]:
        pixels[0].seaborn_neopixel.blink(1, pixels)
    pixels[0].seaborn_neopixel.write()


def _http_get(url, pixels=None):
    _, _, host, path = url.split('/', 3)
    setup_status(pixels, STATUS.ready, 'http get setting up socket')
    addr = socket.getaddrinfo(host, 80)[0][-1]
    conn = socket.socket()
    conn.connect(addr)
    setup_status(pixels, STATUS.set, 'socket connected')
    conn.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host),
                    'utf8'))
    return conn


def http_get(url, pixels=None, buffer_size=100):
    try:
        conn = _http_get(url, pixels)
        data = ''
        while True:
            _data = conn.recv(buffer_size)
            if _data:
                _data = str(_data, 'utf8')
                data += _data
                setup_status(pixels, STATUS.go, _data, end='')
            else:
                break
        conn.close()
        return data
    except Exception as ex:
        setup_status(pixels, STATUS.exception, 'exception: %s' % ex)
        raise


def request_rtc(url='http://micropython.org/ks/test.html', pixels=None,
                buffer_size=100, signpost='Date:', endpost='\n'):
    try:
        conn = _http_get(url, pixels)
        data = ''
        while True:
            _data = conn.recv(buffer_size)
            if not data:
                setup_status(pixels, STATUS.problem, 'no data')
            data += str(_data, 'utf8')
            if not signpost in data:
                continue
            line = data.split(signpost, 1)[-1]
            if not endpost in line:
                continue
            setup_status(pixels, STATUS.go, 'parsing time from: %s'%line)
            line = line.replace(':', ' ')
            _, day, month, year, hour, minute, second = line.split()[:7]
            month = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                     'Jul': 7, 'Aug': 8, 'Sept': 9, 'Nov': 11, 'Dec': 12}.get(
                month)

            break

        try:
            import machine
        except ImportError:
            return

        def _eval(text):
            while text[0] == '0' and text != '0':
                text = text[1:]
            return eval(text)

        rtc = machine.RTC()
        rtc.datetime((_eval(year), month, _eval(day), 0, _eval(hour),
                      _eval(minute), _eval(second), 0))
        setup_status(pixels, STATUS.go, 'datetime set: %s'%str(rtc.datetime()))
    except Exception as ex:
        setup_status(pixels, STATUS.exception, 'exception: %s' % ex)
        raise


def main():
    from seaborn_neopixel import SeabornNeoPixel

    np = SeabornNeoPixel(pin=5, count=50)
    setup_status(np.pixels[0:1], STATUS.ready, 'setup microchip: %s'%NAME)
    connect_to_network(pixels=np.pixels[1:2])
    request_rtc(pixels=np.pixels[2:3])
    setup_status(np.pixels[0:1], STATUS.go, 'setup complete for: %s'%NAME)


if __name__ == '__main__':
    main()
