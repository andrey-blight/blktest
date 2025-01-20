import os
import subprocess

from logger import logger


class GnuPlot:
    GpFileConfig = '''set title "Latency with different IO Depth" font "15"

set xlabel "IO Depth"
set ylabel "Latency (usec)"
set logscale x 2

set terminal pngcairo size 800,600
set output "{output_filename:s}"

set key outside

plot "data.dat" using 1:2 with linespoints title "Read Latency", \
     "data.dat" using 1:3 with linespoints title "Write Latency"'''

    def __init__(self, points: list[tuple[int, float, float]],
                 output_filename: str = "latency_plot.png"):
        self.points = points
        self.output_filename = output_filename

        self._generate_data()  # create .dat file

        self._generate_gnuplot()  # create .gp config file

    def __del__(self):
        os.remove("data.dat")
        os.remove('plot.gp')

        logger.info("Deleted data.dat and plot.gp")

    def _generate_data(self) -> None:
        """
        Generate data.dat file for gnuplot.
        :return: None
        """
        logger.info("Generating data.dat")
        data = "iodepth\tread_latency\twrite_latency\n"
        for point in self.points:
            data += f"{point[0]}\t{point[1]}\t{point[2]}\n"

        with open("data.dat", "w") as file:
            file.write(data)

        logger.debug(f"data.dat: {data}")

    def _generate_gnuplot(self) -> None:
        """
        Generate plot.gp file for gnuplot.
        :return: None
        """
        logger.info("Generating gnuplot.gp")

        text = self.GpFileConfig.format(output_filename=self.output_filename)
        with open("plot.gp", "w") as file:
            file.write(text)

        logger.debug(f"plot.gp: {text}")

    def generate_plot(self):
        logger.info(f"Generating {self.output_filename}")

        res = subprocess.run(["gnuplot", "plot.gp"])

        if res.returncode != 0:
            logger.error(f"Failed to generate {self.output_filename} {res.returncode}")
            raise RuntimeError(f"gnuplot failed with return code: {res.returncode}")
