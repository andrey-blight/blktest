from logger import logger
from FioExecutor import FioExecutor
from GnuPlot import GnuPlot
from functions import generate_parameters, parse_args

IODEPTH = generate_parameters(start=1, stop=256, num_tests=20)

if __name__ == '__main__':
    logger.info("Starting fio test")

    test_name, test_file, plot_output = parse_args()

    fio_executor = FioExecutor(IODEPTH, test_name, test_file)

    latencies = fio_executor.get_latencies()

    print(latencies)

    gnu_plot = GnuPlot(latencies, plot_output).generate_plot()

    logger.info("Finished fio test")
