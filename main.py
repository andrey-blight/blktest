from logger import logger
from FioExecutor import FioExecutor
from GnuPlot import GnuPlot
from functions import generate_parameters

IODEPTH = generate_parameters(start=1, stop=256, num_tests=20)

if __name__ == '__main__':
    logger.info("Starting fio test")

    fio_executor = FioExecutor(IODEPTH)

    latencies = fio_executor.get_latencies()

    print(latencies)

    gnu_plot = GnuPlot(latencies, "latencies.png").generate_plot()

    logger.info("Finished fio test")
