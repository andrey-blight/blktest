FROM python:3.11

# install fio, vim and git
RUN apt-get update && apt-get install -y \
    fio \
    git \
    vim \
    gnuplot \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# clone blktest
RUN git clone https://github.com/andrey-blight/blktest

WORKDIR /workspace/blktest

# add executable to bash
RUN chmod +x blktest

CMD ["./blktest", "-name=blktest", "-filename=file", "-output=static/test.png"]
