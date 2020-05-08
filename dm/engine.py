'''
	@file engine.py
	@module dm
	@author sb
	@date Fri, 08 May 2020 13:01:59 +0530
	@brief module component containing the main engine functions
'''

# standard libs/modules
from os import sep
from collections import namedtuple
from configparser import ConfigParser
from logging import (DEBUG, INFO)

# custom libs/modules
from utility.constants_util import (ERR_TYPE, ERR_VALUE)
from utility.base_util import (setup_logger, create_dir, create_file)
from .dm_exception import (DebugTypeError, DebugValueError)
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
	def __init__(self, enabledbg : bool = False, **kwargs):
		'''
			@function __init__
			@date Fri, 08 May 2020 15:21:39 +0530
			@brief default constructor for Engine class
			@param [IN] gameconf - string containing the path to the game
			configuration file
		'''
		if not isinstance(enabledbg, bool):
			raise DebugTypeError(ERR_TYPE.format("Enable debug", "boolean"))
		elif enabledbg is None:
			raise DebugValueError(ERR_VALUE.format("Boolean"))
		self._dbg_enabled = enabledbg

		self._init = False
		self.engineconf = namedtuple('engineconf',
				'log_fpath, log_fname log_level log_stdio log_fileio')
		self.gameconf = kwargs.get(GAME_CONF_KEY)
		if self.gameconf is not None:
			create_dir("{}".format(self.gameconf[:self.gameconf.rfind(sep)]))
			create_file(self.gameconf)
			self.__parse_config()
		else:
			# write the function for creating the configuration file - like the
			# default location
			pass

		# parse the configuration file and get the details
		self._logger = None

	def set_logger(self):
		# call the setup_logger function here
		pass

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
		cparser = ConfigParser()
		cparser.read(self.gameconf)

		self.engineconf.log_fname = cparser[LOGGER_SECTION][LOGFILE_OPTION]
		self.engineconf.log_fpath = cparser[LOGGER_SECTION][LOGDIR_OPTION]
		self.engineconf.log_fileio = cparser[LOGGER_SECTION][LOGTOFILE_OPTION]
		self.engineconf.log_stdio = cparser[LOGGER_SECTION][LOGTOSTDIO_OPTION]
		self.engineconf.log_level = DEBUG if cparser[ENGINE_SECTION][
				ENABLE_DEBUG_OPTION] == str(ENABLE) else INFO

	def __create_config(self):
		'''
			@function __create_config
			@date Sat, 09 May 2020 00:22:28 +0530
			@brief private member function to create a default configuration
			file
		'''
		cparser = ConfigParser()
		cparser.read(self.gameconf)

		cparser[LOGGER_SECTION] = {}
		cparser[LOGGER_SECTION][LOGFILE_OPTION] = LOGFILE_VALUE
