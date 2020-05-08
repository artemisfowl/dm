'''
	@file engine.py
	@module dm
	@author sb
	@date Fri, 08 May 2020 13:01:59 +0530
	@brief module component containing the main engine functions
'''

# custom libs/modules
from utility.constants_util import (ERR_TYPE, ERR_VALUE)
from utility.base_util import setup_logger
from .dm_exception import (DebugTypeError, DebugValueError)
from .dm_constants import GAME_CONF_KEY

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
		if kwargs.get(GAME_CONF_KEY) is not None:
			print("Config file information : {}".format(kwargs))
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
