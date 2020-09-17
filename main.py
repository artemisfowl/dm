#!/usr/bin/env python

'''
	@file main.py
	@module __main__
	@author sb
	@date Fri, 08 May 2020 11:49:15 +0530
	@brief test for creating a simple engine for writing and checking the
	working of D&D games at runtime - simple as in text based only
'''

# standard libs/modules
from os import (getcwd, sep)
from collections import namedtuple
from sys import (exit, version_info)

# custom libs/modules
from utility.base_util import (create_dir, create_file, parse_args)
from dm.engine import Engine
from dm.dm_exception import(EnableLoggerTypeError, EnableLoggerValueError)

"""
	Todo:
	1. Create an utility module [done]
	2. Create base function for checking existence of dir or file [done]
	3. Create constants to be used in the utility module [done]
	4. Create dm module [done]
	5. Add debugging feature for the program with configparser [done]
	6. Add function for creating a default configuration file if the developer
	has not mentioned about one [done]
	7. make gameconf mandatory [done]
	8. read the logger section and engine debug section is the enable logger is
	set [done]
	9. poll the directory for any changes that might have been done and then
	load the changes to be shown on the screen.
"""

def main():
	'''
		@function main
		@date Wed, 13 May 2020 16:34:59 +0530
		@brief main function, execution starts here
	'''
	try:
		engine_mode_t = namedtuple("engine_mode_t", "gameconf build_mode")
		parse_args(engine_mode_t)

		engine = None
		if engine_mode_t.build_mode:
			# debug mode
			if engine_mode_t.gameconf is not None:
				engine = Engine(gameconf = engine_mode_t.gameconf,
						enable_logger = True)
			else:
				engine = Engine(gameconf = "{}{}config{}game.ini".format(
					getcwd(), sep, sep), enable_logger = True)
		else:
			# release mode
			if engine_mode_t.gameconf is not None:
				engine = Engine(gameconf = engine_mode_t.gameconf)
			else:
				engine = Engine(gameconf = "{}{}config{}game.ini".format(
					getcwd(), sep, sep))

		# start the engine execution
		engine.mainloop()
	except EnableLoggerTypeError as elterr:
		print(elterr)
	except EnableLoggerValueError as elverr:
		print(elverr)
	except Exception as exc:
		print(exc.with_traceback())
	finally:
		print("Exiting engine...")
		return 0

if __name__ == '__main__':
	main()
