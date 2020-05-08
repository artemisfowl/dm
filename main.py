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

# custom libs/modules
from utility.base_util import (create_dir, create_file)
from dm.engine import Engine
from dm.dm_exception import(DebugTypeError, DebugValueError)

"""
	Todo:
	1. Create an utility module [done]
	2. Create base function for checking existence of dir or file [done]
	3. Create constants to be used in the utility module [done]
	4. Create dm module [done]
	5. Add debugging feature for the program with configparser
"""

def main():
	# create an instance of Engine
	# let the engine take care of the config file reading
	# from the config file the logger related information will be picked up
	engine = None

	try:
		engine = Engine(gameconf = "{}{}.config{}game.ini".format(
			getcwd(), sep, sep))
	except DebugTypeError as dbgtypeerr:
		print(dbgtypeerr)
	except DebugValueError as dbgvalerr:
		print(dbgvalerr)

	create_dir("{}{}.config".format(getcwd(), sep))
	create_file("{}{}.config{}game.ini".format(getcwd(), sep, sep))
	return 0

if __name__ == '__main__':
	main()
