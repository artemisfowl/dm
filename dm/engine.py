'''
	@file engine.py
	@module dm
	@author sb
	@date Fri, 08 May 2020 13:01:59 +0530
	@brief module component containing the main engine functions
'''

# standard libs/modules
from os import (sep, stat)
from collections import namedtuple
from configparser import ConfigParser
from logging import (DEBUG, INFO)

# custom libs/modules
from utility.constants_util import (ERR_TYPE, ERR_VALUE)
from utility.base_util import (setup_logger, create_dir, create_file)
from .dm_exception import (EnableLoggerTypeError, EnableLoggerValueError)
from .dm_constants import GAME_CONF_KEY
from .dm_constants import (LOGGER_SECTION, ENGINE_SECTION)
from .dm_constants import (LOGFILE_OPTION, LOGDIR_OPTION, LOGTOFILE_OPTION,
	LOGTOSTDIO_OPTION)
from .dm_constants import (LOGFILE_VALUE, LOGDIR_VALUE, LOGTOFILE_VALUE,
		LOGTOSTDIO_VALUE, ENABLE_DEBUG_VALUE)
from .dm_constants import ENABLE_DEBUG_OPTION
from .dm_constants import (ENABLE, DISABLE)

class Engine:
	'''
		@class Engine
		@date Fri, 08 May 2020 13:03:35 +0530
		@brief Class containing the engine functionality
	'''
	def __init__(self, gameconf : str, enable_logger : bool = False, **kwargs):
		'''
			@function __init__
			@date Fri, 08 May 2020 15:21:39 +0530
			@brief default constructor for Engine class
			@param [IN] gameconf - string containing the path to the game
			configuration file
			enable_logger - boolean flag specifying if the logger has to be
			enabled or not
		'''
		if not isinstance(enable_logger, bool):
			raise EnableLoggerTypeError(ERR_TYPE.format(
				"Enable logger", "boolean"))
		elif enable_logger is None:
			raise EnableLoggerValueError(ERR_VALUE.format("Boolean"))
		self._enable_logger = enable_logger

		self._init = False
		self.engineconf = namedtuple('engineconf',
				'log_fpath, log_fname log_level log_stdio log_fileio')
		self.gameconf = gameconf
		if self.gameconf is not None:
			create_dir("{}".format(self.gameconf[:self.gameconf.rfind(sep)]))
			create_file(self.gameconf)
			if stat(self.gameconf).st_size == 0:
				self.__create_config()
			else:
				self.__parse_config()

		print("Logging information : {}".format(self.engineconf.log_fpath))
		self._logger = None

	def set_logger(self):
		'''
			@function set_logger
			@date Sat, 09 May 2020 23:04:45 +0530
			@brief member function to set up the logger
			@note this function might be removed at a later point of time
		'''
		# call the setup_logger function here
		self._logger = None

	def get_logger(self):
		'''
			@function get_logger
			@date Fri, 08 May 2020 15:21:45 +0530
			@brief member function to get the logger instance
		'''
		return self._logger
	def __parse_config(self):
		'''
			@function __parse_config
			@date Fri, 08 May 2020 22:26:56 +0530
			@brief private member function to parse the configuration file
		'''
		cparser = self.__get_conf_parser()
		cparser.read(self.gameconf)

		self.engineconf.log_fname = cparser[LOGGER_SECTION][LOGFILE_OPTION]
		self.engineconf.log_fpath = cparser[LOGGER_SECTION][LOGDIR_OPTION]
		self.engineconf.log_fileio = True if (
			cparser[LOGGER_SECTION][LOGTOFILE_OPTION] == str(ENABLE)) else (
					False)
		self.engineconf.log_stdio = True if (
			cparser[LOGGER_SECTION][LOGTOSTDIO_OPTION] == str(ENABLE)) else (
					False)
		self.engineconf.log_level = DEBUG if cparser[ENGINE_SECTION][
				ENABLE_DEBUG_OPTION] == str(ENABLE) else INFO

	def __create_config(self):
		'''
			@function __create_config
			@date Sat, 09 May 2020 00:22:28 +0530
			@brief private member function to create a default configuration
			file
		'''
		cparser = self.__get_conf_parser()
		cparser.read(self.gameconf)

		# creating the logger section - call other function
		# TODO : Sun, 10 May 2020 01:22:55 +0530
		cparser[LOGGER_SECTION] = {}
		cparser[LOGGER_SECTION][LOGFILE_OPTION] = str(LOGFILE_VALUE)
		cparser[LOGGER_SECTION][LOGDIR_OPTION] = str(LOGDIR_VALUE)
		cparser[LOGGER_SECTION][LOGTOFILE_OPTION] = str(LOGTOFILE_VALUE)
		cparser[LOGGER_SECTION][LOGTOSTDIO_OPTION] = str(LOGTOSTDIO_VALUE)

		# creating the engine section - call other function
		# TODO : Sun, 10 May 2020 01:23:08 +0530
		cparser[ENGINE_SECTION] = {}
		cparser[ENGINE_SECTION][ENABLE_DEBUG_OPTION] = str(ENABLE_DEBUG_VALUE)

		with open(self.gameconf, "w") as f:
			cparser.write(f)

		self.engineconf.log_fname = LOGFILE_VALUE
		self.engineconf.log_fpath = LOGDIR_VALUE
		self.engineconf.log_fileio = True if LOGTOFILE_VALUE == ENABLE else (
				False)
		self.engineconf.log_stdio = True if LOGTOSTDIO_VALUE == ENABLE else (
				False)
		self.engineconf.log_level = DEBUG if cparser[ENGINE_SECTION][
				ENABLE_DEBUG_OPTION] == str(ENABLE) else INFO

	def __get_conf_parser(self):
		'''
			@function __get_conf_parser
			@date Sun, 10 May 2020 01:21:07 +0530
			@brief private member function to get the config parser object
		'''
		cparser = ConfigParser()

		return cparser
