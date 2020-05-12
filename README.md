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

3. In the terminal itself navigate to the directory where the program is placed.
4. As of now the program is not using any external library. The program can be run using the command `python main.py` or for that matter `python3 main.py`.

**NOTE**: In order to get more information about the program, one can also type `python main.py --help` or `python3 main.py --help`

The help information would be as follows:
```
usage: main.py [-h] [--build-mode BUILD_MODE] [--config CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  --build-mode BUILD_MODE
                        Engine mode has to be in debug(1)
  --config CONFIG       Custom configuration filepath [absolute]
```

So, in order to run the engine in debug mode, just use `python main.py --build-mode 1` or for that matter `python3 main.py --build-mode 1`.

When run in build mode - the logs would be created and a log file containing information would be present in the logs directory.

#### Log information manipulation
When the engine is run, it creates a directory called config where there is a file created by the name of game.ini. The contents of this file are as follows:

```
[logger]
logfile = engine
logdir = logs
logtofile = 1
logtostdio = 0
enabledebug = 1

[engine]
enabledebug = 1
```

##### Game INI options
1. The `logfile` contains the name of the log file which will be created inside the `logdir` directory. In the aforementioned case, the name of the log file would be
`engine_2020-05-12.log`. For each day a new log file would be created so that the debugging mode becomes easier.

A log file, when enabled, would have data as follows:

```
2020-05-12 17:13:53,243 : [MainThread  ][engine.py:72 - __init__() ][INFO ]  Logging information : logs
2020-05-12 17:13:53,243 : [MainThread  ][engine.py:116 - _mainloop() ][INFO ]  Starting the main loop
```

2. The `logtofile` option is enabled by default. This allows for writing the information in the specified log file. If it is set to 0, the logging in the file would not be done.

3. The `logtostdio` option is disabled by default. If this is enabled(value given as 1), the log lines will start showing up in the command prompt or the terminal itself.

4. The `enabledebug` option is an experimental one and will be changed after deliberation as more code is added.
