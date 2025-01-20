import time
import subprocess
import pathlib

from FioParser import FioParser
from logger import logger
from functions import print_progress


class FioExecutor:
    CONFIG_TEXT = """[global]
name={test_name:s}
ioengine=libaio
direct=1
bs=4k
size=1G
numjobs=1
iodepth={iodepth:d}

[read_test]
filename={filename:s}
rw=randread

[write_test]
filename={filename:s}
rw=randwrite"""

    def __init__(self, iodepth_array: list[int], test_name: str, filename: str):
        for iodepth in iodepth_array:
            if iodepth > 256 or iodepth < 1:
                raise ValueError("iodepth must be between 1 and 256")

        self.iodepth_array = iodepth_array
        self.test_name = test_name
        self.filename = filename

    def _create_config_file(self, iodepth: int) -> pathlib.Path:
        """
        Create fio config file for transmitted commands

        :param iodepth: iodepth param for fio config file
        :return: Path to fio config file
        """
        config_text = self.CONFIG_TEXT.format(iodepth=iodepth,
                                              test_name=self.test_name,
                                              filename=self.filename)

        with open("config.fio", "w") as config_file:
            config_file.write(config_text)

        logger.info("Created fio config file")
        logger.debug(f"fio config file: {config_text}")

        return pathlib.Path("config.fio")

    def _execute_fio(self, iodepth: int) -> str:
        """
        Start fio as subprocess and return it stdout.
        :param iodepth: iodepth of fio.
        :return: fio execution result.
        """

        # create fio file with custom parameters
        config_path = self._create_config_file(iodepth)

        try:
            logger.info(f"start fio with iodepth={iodepth}")

            # run fio with config file as subprocess
            start_time = time.time()
            result = subprocess.run(
                ["fio", config_path.name],
                text=True,
                capture_output=True,
                check=True
            )
            end_time = time.time()

            # logging fio execution time
            logger.info(f"fio execution time: {end_time - start_time} seconds")

            config_path.unlink()  # delete config file

            return result.stdout

        except subprocess.CalledProcessError:
            logger.error("subprocess.CalledProcessError", exc_info=True)

            config_path.unlink()  # delete config file

            raise RuntimeError("fio execution failed")

    def get_latencies(self) -> list[tuple[int, float, float]]:
        """
        Execute fio with different iodepth and return latencies

        :return: list of latencies (iodepth, read latency, write latency)
        """

        latencies = []

        for i, iodepth in enumerate(self.iodepth_array):
            print_progress(i + 1, len(self.iodepth_array))

            fio_text = self._execute_fio(iodepth)  # run fio with current iodepth

            # parse latency from stdout
            fio_parser = FioParser(fio_text)
            read_latency, write_latency = fio_parser.parse()

            latencies.append((iodepth, read_latency, write_latency))  # save iodepth and latency

        return latencies
