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

"""
	Todo:
	1. Create an utility module [done]
	2. Create base function for checking existence of dir or file
"""

def main():
	create_dir("{}{}.config".format(getcwd(), sep))
	create_file("{}{}.config{}game.ini".format(getcwd(), sep, sep))
	return 0

if __name__ == '__main__':
	try:
		main()
	except Exception as exc:
		print(exc)
