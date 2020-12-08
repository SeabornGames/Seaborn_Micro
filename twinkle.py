from seaborn_neopixel import (SeabornNeoPixel, randint, SeabornEngine,
                              SeabornTransition)


def main(count=100, rand_count=20, max_step=10, pin=5, update_rate=0.5):
    np = SeabornNeoPixel(count=count, pin=pin, update_rate=update_rate)
    colors = np.get_colors('GREEN', 'RED')
    indexes = []
    engine = SeabornEngine()

    def rand_color():
        return list(colors[randint(0, len(colors))])

    def get_transition():
        index = np.get_random_pixel_indexes(deprioritized_pixels=indexes)[0]
        indexes.append(index)
        step = randint(2, max_step)
        old = index_color[index]
        return SeabornTransition(np=np,
                                 index=index,
                                 colors=[
                                     old,
                                     [old[0] // 2, old[1] // 2, old[2] // 2],
                                     [255, 255, 255],
                                     rand_color(),
                                 ],
                                 steps=[step, 1, step * 2])

    index_color = []
    for i in range(count):
        index_color.append(rand_color())
        np[i] = tuple(index_color[-1])

    for i in range(rand_count):
        engine.append(get_transition())

    while np.running:
        for threads_done in engine:
            for t in threads_done:
                if t is None:
                    continue
                np[t.index] = tuple(t.colors[-1])
                index_color[t.index] = t.colors[-1]
                engine.threads.remove(t)
                indexes.remove(t.index)
                engine.append(get_transition())
            np.write()
            np.sleep()
            print(len(engine.threads))


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception:
            pass
