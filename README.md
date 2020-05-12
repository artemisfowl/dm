## dm
DM is a simple attempt at creating a game engine - preferably as simple as possible for the dungeons and dragons genre. The display has not been yet covered/decided, but the aim is to create a
program, as of now a proof of concept program which will allow for loading of assets as well as game content without having to launch the engine again and again.

#### Program working modes
The program would be running in 2 modes:
1. **Release** - This is the default mode of the program/engine. The program will read from a packed file(_TBD_) and then the game will be handled from the program/engine side.
2. **Debug** - This mode is the one where the program will allow for the development of a D&D game from scratch. This is the mode in which the resources would be loaded automatically and shown on the
	 screen as and when added.

#### Running the program
There are no restrictions on the version of Python to be used other than the fact that the program leverages a few standard modules from the Python3 library.
In order to run the program/engine, one can follow these steps:
1. Open up terminal(Linux/Mac) or command prompt(Windows).
2. In **Windows** check if python is present in the environment variables or not. If it is not, kindly add the same. For **Linux/Mac**, check the version of python being used with the command
`python --version`.
The python interpreter can be downloaded and installed from [here](https://www.python.org/).
__NOTE__: Please note that in Linux, Python 3.x is present already most probably, so kindly get the version using the command `python3 --version` in the terminal.
