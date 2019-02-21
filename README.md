# beatclay
A smart bracelet making moving to music more engaging. This device was built to enhance an audience's collective interaction with a live coding performance. By aggregating and mapping accelerometer and gyroscope data to tempo and volume parameters in the live coding environment, the audience can drive elements of the music in real-time. The device also aims to create engaging interaction within audience members, as the level of synchronicity in their movements affect the intensity of the effects in the music.

## Getting Started
There are three components to this project. The microcontroller client-code, the python server-code and the modified extempore vscode extension. 

##### Hardware Requirements: 
- nodeMCU v0.9 with ESP12E wifi module or ESP8266 (Lolin and Amica were used in this project)
- Arduino MPU6050 

##### Software Requirements: 
- Python 3.6.3
    - pip
    - pipenv
    - numpy 
    - websockets
- npm and yo code for vscode extension install
- Extempore Live Coding environment
- CH340G driver for Lolin microcontroller OR CP2101 driver for the Amica board
- vscode editor


Begin by cloning the repository.

#### Microcontroller setup
1. Connect the hardware components according to the image below. Power can be supplied via USB or battery (3v to 3.6v) 
![Circuit Diagram](/assets/readme_images/connect_accelto_node.jpg "Circuit Diagram")
2. To deploy code to microcontroller, you need to install the [Arduino IDE](https://www.arduino.cc/en/main/software). 
3. Install the board manager for ESP8266 in the Arduino IDE. Here are some [instructions](https://www.instructables.com/id/Steps-to-Setup-Arduino-IDE-for-NODEMCU-ESP8266-WiF/) on how to do that.
4. Install the appropriate drivers for your microcontroller. The drivers for the [Lolin](https://sparks.gogo.co.nz/ch340.html) and [Amica](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers) nodeMCU boards were used in this project. 
5. Connect the board to your machine and navigate to Tools > Port in your Arduino IDE. Select the port for your device driver. This port number can be found under Device Manager > Ports.
6. Set the Upload Speed (Tools > Upload Speed) to 57600bps. 
7. Verify, then upload the code to the board. 

#### Python setup
1. If you haven't already, you will need to install [Python](https://www.python.org/downloads/) and [pip](https://www.makeuseof.com/tag/install-pip-for-python/) on your machine.
2. Run `pip install pipenv` to install pipenv.
2. Create a virtual env with Python 3.6.3 by running the following command within the src directory. 
    `pipenv --python 3.6.3`
3. Activate your virtual environment with `pipenv shell` and install the following dependencies with `pip install <dependency-name>`.
    - numpy
    - websockets

#### Extension Setup
1. This device is used in conjunction with the Extempore live coding environment. [Install](https://extemporelang.github.io/docs/overview/install/) and setup the Extempore environment and refer to the [Extempore Documentation](https://extemporelang.github.io/docs/) for guides and examples. A very simple example of a looped C minor arpeggio chord has been provided in the examples diretory. To run this, begin an Extempore session and evaluate the setup.xtm code and the livecode_IoT.xtm code (either all at once or line by line). 
2. Install [vscode](https://code.visualstudio.com/docs/setup/setup-overview).
3. Install the extension in vscode by running `code --install-extension my-extension-0.0.1.vsix` from the root directory of this repo. This extension is a modified version of the vscode-extempore 0.0.9 extension.

**IMPORTANT NOTE**: the following lines of code must be evaluated in an Extempore session which is intended to be used with beatclays. 
`(define *metro* (make-metro <tempo-in-bpm>))`
`(define vol1 60)`. 

The vscode extension will update the value of *vol1* and the tempo of *\*metro\**, so this naming convention is important. Use the variable *vol1* in place of any volume value you wish to control with beatclays.

## Developers

## Contact Information
For any questions regarding this project, contact me on 