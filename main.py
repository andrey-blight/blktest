from logger import logger
from FioExecutor import FioExecutor

IODEPTH = list(range(1, 256, 100))

if __name__ == '__main__':
    logger.info("Starting fio test")

    fio_executor = FioExecutor(IODEPTH)

    latencies = fio_executor.get_latencies()
    print(latencies)
    logger.info("Finished fio test")
