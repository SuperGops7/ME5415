# ME5415 AY2024/2025 Project 

# Pipe Robot Locomotion
After initial environment setup steps, in this ```/proj``` directory

        git clone https://github.com/csesarah/ME5415.git
        cd ME5415
        ./sofa/build/bin/runSofa src/main.py

---

# Environment Setup

## Install SOFA

### Dependencies

        sudo apt upgrade && sudo apt update
        sudo apt install git curl
        sudo apt install build-essential software-properties-common
        sudo apt install gcc-12
        sudo apt install clang-15
        sudo apt install ccache
        sudo apt install cmake cmake-gui
        sudo apt install libopengl0 
        sudo apt install python3-pip pybind11-dev
        sudo apt install libtinyxml2-dev
        sudo apt install libboost-all-dev
        sudo apt install libeigen3-dev
        sudo apt install xorg-dev libgtk-3-dev
        sudo apt install libgl1-mesa-dev
        sudo apt install libpng-dev libjpeg-dev libtiff-dev libglew-dev zlib1g-dev
        sudo apt install nvidia-cuda-toolkit
        sudo apt install -y qtcreator qtbase5-dev qt5-qmake 
        sudo apt install libgtest-dev
        python3 -m pip install pip==21.0
        python3 -m pip install numpy==1.26.4 scipy pybind11==2.9.1

### Download
Download SOFA repo and set up file directory structure

        git clone -b v23.06 https://github.com/sofa-framework/sofa.git sofa/src
        cd sofa
        mkdir build

Download plugins into ```plugins``` directory

        mkdir plugins
        cd plugins
        git clone https://github.com/SofaDefrost/SPLIB
        git clone -b v23.06 https://github.com/SofaDefrost/STLIB
        git clone -b v23.06 https://github.com/SofaDefrost/SoftRobots
        git clone -b v23.06 https://github.com/SofaDefrost/ModelOrderReduction
        git clone -b v23.06 https://github.com/SofaDefrost/Cosserat
        git clone -b v23.06 https://github.com/sofa-framework/BeamAdapter

### Build

1. Create ```CMakeLists.txt``` file in ```plugins``` directory as follows:

        cmake_minimum_required(VERSION 3.22)

        find_package(SofaFramework)

        sofa_add_subdirectory(plugin Cosserat/  Cosserat)
        sofa_add_subdirectory(plugin ModelOrderReduction/  ModelOrderReduction)
        sofa_add_subdirectory(plugin SoftRobots/  SoftRobots)
        sofa_add_subdirectory(plugin SPLIB/  SPLIB)
        sofa_add_subdirectory(plugin STLIB/  STLIB)

2. Generate Makefile

       cmake-gui

3. Set generator as ```Unix Makefiles``` and select ```Use default native compilers```
4. Set source folder as ```sofa/src``` and build folder as ```sofa/build```
5. Run **Configure** and set the following parameters:

        SOFA_FETCH_BEAMADAPTER=ON
        SOFA_FETCH_SOFAPYTHON3=ON
        SOFA_EXTERNAL_DIRECTORIES=/PATH_TO/proj/plugins

6. Run **Configure** again and ensure that the following parameters are set as follows:

        PLUGIN_SOFAPYTHON3=ON
        PLUGIN_BEAMADAPTER=ON
        PLUGIN_COSSERAT=ON
        PLUGIN_SPLIB=ON
        PLUGIN_STLIB=ON
        PLUGIN_SOFTROBOTS=ON
        PLUGIN_MODELORDERREDUCTION=ON

7. Run **Generate**
8. Build

        cd build
        make

9. Load plugins

        cp lib/plugin_list.conf.default lib/plugin_list.conf
        ls lib | grep plugin
        echo -e "\nSofaPython3 NO_VERSION" >> lib/plugin_list.conf
        cat lib/plugin_list.conf

### Run

     ./bin/runSofa

---

## Install SofaGym

### Download

        git clone https://github.com/SofaDefrost/SofaGym

### Dependencies

        python3 -m pip install setuptools==65.5.0 
        python3 -m pip install wheel==0.38.0
        python3 -m pip install gym==0.21.0
        python3 -m pip install stable-baselines3[extra]==1.7.0
        python3 -m pip install rlberry==0.5.0
        python3 -m pip install psutil pygame glfw pyopengl imageio imageio-ffmpeg
        python3 -m pip install tensorboard

        export SOFA_ROOT=$(pwd)/sofa/build/
        export PYTHONPATH=$(pwd)/sofa/build/lib/python3/site-packages:$PYTHONPATH

        cd SofaGym
        python3 setup.py bdist_wheel
        python3 -m pip install -v -e .

### Run

        python3 test_env.py -e trunk-v0 -ep 100 -s 100
        python3 rl.py -e trunk-v0 -a PPO


