import subprocess
import time

from logger import logger

FIO_CONFIG = "test.fio"


def execute_fio(iodepth: int = 1) -> str:
    start_time = time.time()

    try:
        logger.info(f"start fio with iodepth={iodepth}")

        result = subprocess.run(
            ["fio", FIO_CONFIG],
            text=True,
            capture_output=True,
            check=True
        )

        end_time = time.time()
        logger.info(f"fio execution time: {end_time - start_time} seconds")

        return result.stdout

    except subprocess.CalledProcessError as e:
        logger.error("subprocess.CalledProcessError", exc_info=True)
        exit(1)


def parse_output(fio_output: str) -> tuple[float | None, float | None]:
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
                return None, None

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


if __name__ == '__main__':
    # logger.info("Starting fio test")
    # fio_response = execute_fio()
    #
    # print("FIO Output:")
    # print(fio_response)

    with open("fio_response.txt", "r") as file:
        fio_response = file.read()

    print(parse_output(fio_response))
