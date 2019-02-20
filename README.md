# beatclay
A smart bracelet making moving to music more engaging. This device was built to enhance an audience's collective interaction with a live coding performance. By aggregating and mapping accelerometer and gyroscope data to tempo and volume parameters in the live coding environment, the audience can drive elements of the music in real-time. The device also aims to create engaging interaction within audience members, as the level of synchronicity in their movements affect the intensity of the effects in the music.

## Getting Started
There are three components to this project. The microcontroller client-code, the python server-code and the modified extempore vscode extension. 

#### Python setup
1. clone the repository
2. You will need to set up a virtual env within the src folder. I used [pipenv](https://pipenv.readthedocs.io/en/latest/) with python 3.6. 
3. Activate your virtual environment and install the following dependencies. (You may need to install [pip](https://www.makeuseof.com/tag/install-pip-for-python/) if you haven't already.) 
    - numpy
    - websockets

Hardware You will need: 
- nodeMCU v0.9 with ESP12E wifi module or ESP8266
- Arduino MPU6050 

Software tools: 
- python 
- npm and yo code for vscode extension install
- extempore language

