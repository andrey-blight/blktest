import re

from logger import logger


class FioParser:
    # regex pattern to parse latency line
    LATENCY_PATTERN = r"^\s*lat\s+\((\w+)\).*?avg=\s*([\d.]+)"

    # lambdas to convert time to usec
    TIME_CONVERSION = {
        "msec": lambda msec: msec * 1000,
        "usec": lambda usec: usec,
        "nsec": lambda nsec: nsec * 0.001
    }

    def __init__(self, fio_stdout: str):
        self.fio_stdout = fio_stdout
        # split by lines and remove left and right spaces
        self.stdout_lines = [el.strip() for el in fio_stdout.split("\n")]

    def parse(self) -> tuple[float, float]:
        """
        Get average latency from fio output for write and read commands in usec

        :return: read latency, write latency
        """
        logger.debug(f"fio output: {self.fio_stdout}")
        logger.info("start parsing fio output")

        read_latency = None
        write_latency = None
        operation_type = None  # determine what command is now

        for line in self.stdout_lines[2:]:  # skip first two lines about test params

            regex_result = re.search(self.LATENCY_PATTERN, line)  # check is this latency line

            if line.startswith("read_test"):  # if now read_test logs
                operation_type = "read"
            elif line.startswith("write_test"):  # if now write test logs
                operation_type = "write"
            elif regex_result:  # if this line contains average latency

                unit = regex_result.group(1)  # (msec), (nsec), (usec)
                avg = float(regex_result.group(2))
                usec_avg = self.TIME_CONVERSION[unit](avg)  # convert time in usec

                match operation_type:
                    case "read":
                        read_latency = usec_avg
                        logger.info(f"read latency: {read_latency}")
                    case "write":
                        write_latency = usec_avg
                        logger.info(f"write latency: {write_latency}")

        return read_latency, write_latency


if __name__ == '__main__':
    with open("test.txt") as file:
        fio_stdout = file.read()

    print(FioParser(fio_stdout).parse())
