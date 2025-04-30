# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl build-essential software-properties-common \
    gcc-12 clang-15 ccache cmake cmake-gui \
    libopengl0 python3-pip pybind11-dev libtinyxml2-dev \
    libboost-all-dev libeigen3-dev xorg-dev libgtk-3-dev \
    libgl1-mesa-dev libpng-dev libjpeg-dev libtiff-dev \
    libglew-dev zlib1g-dev nvidia-cuda-toolkit \
    qtcreator qtbase5-dev qt5-qmake libgtest-dev \
 && rm -rf /var/lib/apt/lists/*

# Python dependencies
RUN python3 -m pip install --upgrade pip==21.0 && \
    python3 -m pip install numpy==1.26.4 scipy pybind11==2.9.1 \
        setuptools==65.5.0 wheel==0.38.0 gym==0.21.0 \
        stable-baselines3[extra]==1.7.0 rlberry==0.5.0 \
        psutil pygame glfw pyopengl imageio imageio-ffmpeg tensorboard

# Create working directory
WORKDIR /proj
COPY . /proj

# Clone and build SOFA + plugins
RUN git clone -b v23.06 https://github.com/sofa-framework/sofa.git sofa/src && \
    mkdir -p sofa/build && mkdir -p sofa/plugins && \
    cd sofa/plugins && \
    git clone https://github.com/SofaDefrost/SPLIB && \
    git clone -b v23.06 https://github.com/SofaDefrost/STLIB && \
    git clone -b v23.06 https://github.com/SofaDefrost/SoftRobots && \
    git clone -b v23.06 https://github.com/SofaDefrost/ModelOrderReduction && \
    git clone -b v23.06 https://github.com/SofaDefrost/Cosserat && \
    git clone -b v23.06 https://github.com/sofa-framework/BeamAdapter

COPY docker/CMakeLists_plugins.txt /proj/sofa/plugins/CMakeLists.txt

# Set environment
ENV SOFA_ROOT=/proj/sofa/build
ENV PYTHONPATH=/proj/sofa/build/lib/python3/site-packages:$PYTHONPATH

# Clone and install SofaGym
RUN git clone https://github.com/SofaDefrost/SofaGym && \
    cd SofaGym && python3 setup.py bdist_wheel && \
    python3 -m pip install -v -e .

# Default to project folder
WORKDIR /proj

CMD ["/bin/bash"]
