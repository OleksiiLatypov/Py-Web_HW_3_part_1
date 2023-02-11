from time import time
from multiprocessing import cpu_count, Pool
import logging


def factorize(*args: int) -> dict:
    output = {i: [j for j in range(1, i + 1) if i % j == 0] for i in args}
    return output


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    processors = cpu_count()
    start = time()
    result = factorize(128, 255, 99999, 10651060)
    logging.info(f'time using one stream: {time() - start}')
    for k,v in result.items():
        print(f'{k}: {v}')
    print()
    start_pool = time()
    pool = Pool(processors)
    result = pool.apply_async(factorize, (128, 255, 99999, 10651060))
    logging.info(f'time using multiprocessing on {processors} processors: {time() - start_pool}')
    for k, v in result.get().items():
        print(f'{k}: {v}')


