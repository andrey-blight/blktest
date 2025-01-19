FROM python:3.11

# install fio and git
RUN apt-get update && apt-get install -y \
    fio \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# clone blktest
RUN git clone https://github.com/andrey-blight/blktest

WORKDIR /workspace/blktest
