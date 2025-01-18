import time
import subprocess
import pathlib

from logger import logger


class FioExecutor:
    CONFIG_TEXT = """[global]
name=mytest
ioengine=posixaio
direct=1
bs=4k
size=1G
numjobs=1
iodepth={iodepth:d}

[read_test]
filename=test_file
rw=randread

[write_test]
filename=test_file
rw=randwrite"""

    def __init__(self, iodepth_array: list[int]):
        for iodepth in iodepth_array:
            if iodepth > 256 or iodepth < 1:
                raise ValueError("iodepth must be between 1 and 256")

        self.iodepth_array = iodepth_array

    def _create_config_file(self, iodepth: int) -> pathlib.Path:
        """
        Create fio config file for transmitted commands

        :param iodepth: iodepth param for fio config file
        :return: Path to fio config file
        """
        config_text = self.CONFIG_TEXT.format(iodepth=iodepth)

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

    @staticmethod
    def _parse_output(fio_output: str) -> tuple[float, float]:
        """
        Get average latency from fio output for write and read commands

        :param fio_output: stdout from fio
        :return: read latency, write latency
        """
        logger.debug(f"fio output: {fio_output}")
        logger.info("start parsing fio output")

        # split by lines and remove left and right spaces
        result_text = [el.strip() for el in fio_output.split("\n")]

        read_latency = None
        write_latency = None
        operation_type = None  # determine what command is now
        for line in result_text[2:]:

            if line.startswith("read_test"):  # if now read_test logs
                operation_type = "read"
            elif line.startswith("write_test"):  # if now write test logs
                operation_type = "write"
            elif line.startswith("lat (usec):"):  # if this line contains average latency
                lat_avg = ""  # save here latency

                i = line.find("avg=") + len("avg=")  # find str index, where average value

                # check if "avg=" was found
                if i == -1:
                    logger.error(f"Cannot find avg= in line: {line}")
                    raise ValueError(f"Cannot find avg= in line: {line}")

                while line[i] != ',':
                    lat_avg += line[i]
                    i += 1

                lat_avg = float(lat_avg)

                match operation_type:
                    case "read":
                        read_latency = lat_avg
                        logger.info(f"read latency: {read_latency}")
                    case "write":
                        write_latency = lat_avg
                        logger.info(f"write latency: {write_latency}")

        return read_latency, write_latency

    def get_latencies(self) -> list[tuple[int, float, float]]:
        """
        Execute fio with different iodepth and return latencies

        :return: list of latencies (iodepth, read latency, write latency)
        """

        latencies = []

        for iodepth in self.iodepth_array:
            fio_text = self._execute_fio(iodepth)  # run fio with current iodepth

            read_latency, write_latency = self._parse_output(fio_text)  # parse latency from stdout

            latencies.append((iodepth, read_latency, write_latency))  # save iodepth and latency

        return latencies
