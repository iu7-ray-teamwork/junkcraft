import time


def time_steps(desired_step):
    previous = time.perf_counter()
    while True:
        current = time.perf_counter()
        step = current - previous
        if step < desired_step:
            continue
        yield step
        previous = current
