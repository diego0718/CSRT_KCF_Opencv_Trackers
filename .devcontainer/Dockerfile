FROM ubuntu:20.04

# non-root user 
ARG USERNAME=dhernandez
ARG USER_UID=1000
ARG USER_GID=$USER_UID

#Avoid warinings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libopencv-dev \
        libprotobuf-dev \
        libsnappy-dev \
        protobuf-compiler \
        python3-dev \
        python3-numpy \
        python3-pip \
        python3-setuptools \
        python3-scipy && \
    # Create the user
    groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    # Clean up
    apt-get autoremove && apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Setting up working directory 
RUN mkdir /epicio_tracker
WORKDIR /epicio_tracker
# Install Opencv contrib(include tracking library):
COPY ../requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

#CMD ["/python3", "main.py", "--tracker", "KCF"]

