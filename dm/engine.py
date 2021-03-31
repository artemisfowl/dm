'''
	@file engine.py
	@module dm
	@author sb
	@date Fri, 08 May 2020 13:01:59 +0530
	@brief module component containing the main engine functions
'''

# standard libs/modules
from os import (sep, stat, listdir)
from collections import namedtuple
from configparser import ConfigParser
from logging import (DEBUG, INFO)
from logging import exception
from datetime import datetime
from sys import exit

from logging import RootLogger

# custom libs/modules
from utility.constants_util import (ERR_TYPE, ERR_VALUE)
from utility.base_util import (setup_logger, create_dir, create_file)
from .dm_exception import (EnableLoggerTypeError, EnableLoggerValueError)
from .dm_constants import GAME_CONF_KEY
from .dm_constants import (LOGGER_SECTION, ENGINE_SECTION)
from .dm_constants import (LOGFILE_OPTION, LOGDIR_OPTION, LOGTOFILE_OPTION,
	LOGTOSTDIO_OPTION)
from .dm_constants import (READ_RES_DIR_OPTION, READ_RES_DBG_DIR_OPTION,
		READ_RES_REL_DIR_OPTION)
from .dm_constants import (LOGFILE_VALUE, LOGDIR_VALUE, LOGTOFILE_VALUE,
		LOGTOSTDIO_VALUE, ENABLE_DEBUG_VALUE)
from .dm_constants import (READ_RES_DIR_VALUE, READ_RES_DBG_DIR_VALUE,
		READ_RES_REL_DIR_VALUE)
from .dm_constants import ENABLE_DEBUG_OPTION
from .dm_constants import (ENABLE, DISABLE)
from .dm import Dm

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
				'{} {} {} {} {} {} {} {}'.format("log_fpath", "log_fname",
					"log_level", "log_stdio", "log_fileio",
					"readresdir", "debugdir", "releasedir"))
		self.gameconf = gameconf
		if self.gameconf is not None:
			create_dir("{}".format(self.gameconf[:self.gameconf.rfind(sep)]))
			create_file(self.gameconf)

			if stat(self.gameconf).st_size == 0:
				self.__create_config()
			else:
				# first of all - read the logger information if the debug mode
				# is enabled
				self.__parse_config()

		self._logger = None
		if self._enable_logger:
			self.set_logger()
			self._logger.info("Logging information : {}".format(
				self.engineconf.log_fpath))

		self._dm = None
		self.dbgp = None
		self.relp = None
		self.sel_dbgp = None
		self.sel_relp = None
		self.run = True

	def set_logger(self):
		'''
			@function set_logger
			@date Sat, 09 May 2020 23:04:45 +0530
			@brief member function to set up the logger
			@note this function might be removed at a later point of time
		'''
		create_dir(self.engineconf.log_fpath)

		self._logger = setup_logger(log_fpath = self.engineconf.log_fpath,
				log_fname = "{}_{}.log".format(self.engineconf.log_fname,
					datetime.now().date()),
				log_level = self.engineconf.log_level,
				log_stdio = self.engineconf.log_stdio,
				log_fileio = self.engineconf.log_fileio)

	def get_logger(self):
		'''
			@function get_logger
			@date Fri, 08 May 2020 15:21:45 +0530
			@brief member function to get the logger instance
		'''
		return self._logger

	def mainloop(self):
		'''
			@function mainloop
			@date Tue, 12 May 2020 16:35:44 +0530
			@brief member function to start the main loop
		'''
		while self.run:
			self.__mainloop()

	def __load_projects(self):
		'''
			@function __load_projects
			@date Tue, 18 Aug 2020 21:26:44 +0530
			@brief function to list the projects present in the debug or
			release directory
		'''

		# Thu, 17 Sep 2020 08:32:03 +0530 : the problem is that the parent
		# directory is not created - ./parent/debug or release directory
		if self._enable_logger:
			self.dbgp = listdir("{}{}{}".format(
				self.engineconf.readresdir, sep,
				self.engineconf.debugdir))
			self._logger.debug("Projects in dev : {}".format(self.dbgp))
		else:
			self.relp = listdir("{}{}{}".format(
				self.engineconf.readresdir, sep,
				self.engineconf.releasedir))

	def choose_project(self):
		'''
			@function choose_project
			@date Tue, 18 Aug 2020 22:11:15 +0530
			@brief function to allow the user to choose a project or create a
			new one
		'''
		self.__load_projects()

		initial_choice = [
				"Create new project.",
				"Choose an existing project.",
				]
		while True:
			for i in initial_choice:
				print("{}. {}".format(initial_choice.index(i) + 1, i))

			print("[Please enter the option number]")
			# Fri, 18 Sep 2020 22:08:39 +0530 : prompt needs to be changed
			choice = int(input(">>> "))

			if choice == 1:
				if self._enable_logger:
					# engine running in debugging mode
					self._logger.debug("Need new project name")
				self.__set_project_name(iname = input("project name >_ "))
			elif choice == 2:
				if self._enable_logger:
					# engine running in debugging mode
					self._logger.debug("List of projects found : {}".format(
						self.dbgp))

				# show the list of projects found
				self.__show_projects()

			# create the project directory here
			if self._enable_logger:
				if self.sel_dbgp is not None:
					break
			else:
				if self.sel_relp is not None:
					break

	def __show_projects(self):
		'''
			@function __show_projects
			@date Wed, 19 Aug 2020 09:04:23 +0530
			@brief function to show the detected projects
		'''

		while True:
			if self._enable_logger:
				# this is the debugging mode
				self.__show_list(lname = self.dbgp)

				if self.sel_dbgp is None:
					sp_choice = int(input("select project >~ "))
					self.sel_dbgp = self.dbgp[sp_choice - 1]
					self._logger.debug("Chosen project name : {}".format(
						self.sel_dbgp))
			else:
				# this is the release mode
				self.__show_list(lname = self.relp)

				if self.sel_relp is None:
					sp_choice = int(input("select project >~ "))
					self.sel_relp = self.relp[sp_choice - 1]

			if self._enable_logger:
				self._logger.debug("Selected project : {}".format(
					self.sel_dbgp))
				if self.sel_dbgp is not None:
					break
			else:
				if self.sel_relp is not None:
					break

	def __show_list(self, lname = None):
		'''
			@function __show_list
			@date Wed, 19 Aug 2020 09:06:20 +0530
			@brief function to show the list contencts on the screen
		'''
		if lname is None or not isinstance(lname, list):
			return

		if len(lname) > 0:
			for i in lname:
				print("{}. {}".format(lname.index(i) + 1, i))
		else:
			print("No projects present, plese create a new one")
			# Wed, 19 Aug 2020 13:15:26 +0530 - debating whether the user
			# should be allowed to create it from here or create from the debug
			# projects
			self.__set_project_name(iname = input("project name >_ "))

	def __set_project_name(self, iname):
		'''
			@function __set_project_name
			@date Wed, 19 Aug 2020 08:54:00 +0530
			@brief function for setting the project name
		'''
		if self._enable_logger:
			self.sel_dbgp = iname
			self._logger.debug("Project name given : {}".format(iname))
			self._logger.debug("Creating project fullpath : {}{}{}{}{}".format(
					self.engineconf.readresdir, sep,
					self.engineconf.debugdir, sep,
					self.sel_dbgp))
			create_dir("{}{}{}{}{}".format(
					self.engineconf.readresdir, sep,
					self.engineconf.debugdir, sep,
					self.sel_dbgp))
		else:
			self.sel_relp = iname
			create_dir("{}{}{}{}{}".format(
					self.engineconf.readresdir, sep,
					self.engineconf.releasedir, sep,
					self.sel_relp))

	def __mainloop(self):
		'''
			@function _mainloop
			@date Tue, 12 May 2020 16:18:08 +0530
			@brief private member function to start the main loop and handle
			exit criteria
		'''
		try:
			# set the directory to be monitored - if the mode of the engine is
			# debug, else set the zip file option for reading the released
			# version of the game

			self.choose_project()

			if self._enable_logger:
				self._logger.debug("Final debug path : {}{}{}{}{}".format(
					self.engineconf.readresdir, sep,
					self.engineconf.debugdir, sep,
					self.sel_dbgp))
			else:
				print("Final release path : {}{}{}{}{}".format(
					self.engineconf.readresdir, sep,
					self.engineconf.releasedir, sep,
					self.sel_relp))

			# Sun, 20 Sep 2020 10:53:03 +0530 : This dm shoudl be setup with
			# the right directory location as well as the right logger if it is
			if self._enable_logger:
				self._logger.debug("Final debug path : {}{}{}{}{}".format(
					self.engineconf.readresdir, sep,
					self.engineconf.debugdir, sep,
					self.sel_dbgp))
				self._dm = Dm(readdir = "{}{}{}{}{}".format(
					self.engineconf.readresdir, sep,
					self.engineconf.debugdir, sep,
					self.sel_dbgp), logger = self._logger)
			else:
				self._dm = Dm(readdir = "{}{}{}{}{}".format(
					self.engineconf.readresdir, sep,
					self.engineconf.releasedir, sep,
					self.sel_relp))

			if self._enable_logger:
				self._logger.debug("Value of dm : {}".format(
					self._dm.__dict__))

			# this logging function needs to be streamlined
			if self._enable_logger:
				self._logger.info("Starting the main loop")

			self._dm.init_watch()
			while True:
				# Thu, 01 Apr 2021 00:33:17 +0530 : DM will be handling the UI
				# as well as the things to be shown in the UI(user facing)
				self._dm.manage()
				self._dm.update()
		except KeyboardInterrupt as kinterrupt:
			choice = input("Are you sure you want to exit? [Y/n] : ")
			if isinstance(choice, str):
				if choice == "":
					exit("Engine exiting")
				elif choice.lower()[0] == 'y':
					exit("Engine exiting")
		except Exception as exc:
			if self._enable_logger:
				exception(exc)
		finally:
			if self._enable_logger:
				self._logger.debug("Cleaning up pygame instance")
			if self._dm:
				self._dm.cleanup()

			self._dm.stop_observer()
			self.run = False

	def __parse_config(self):
		'''
			@function __parse_config
			@date Fri, 08 May 2020 22:26:56 +0530
			@brief private member function to parse the configuration file
		'''
		cparser = self.__get_conf_parser()
		cparser.read(self.gameconf)

		# read the logger section if debug mode is enabled for the engine
		if self._enable_logger:
			self.engineconf.log_fname = cparser[LOGGER_SECTION][LOGFILE_OPTION]
			self.engineconf.log_fpath = cparser[LOGGER_SECTION][LOGDIR_OPTION]
			self.engineconf.log_fileio = True if (
				cparser[
					LOGGER_SECTION][LOGTOFILE_OPTION] == str(ENABLE)) else (
						False)
			self.engineconf.log_stdio = True if (
				cparser[LOGGER_SECTION][
					LOGTOSTDIO_OPTION] == str(ENABLE)) else (
						False)
			self.engineconf.log_level = DEBUG

		# read the engine section - the debug directory to be read
		self.engineconf.readresdir = cparser[ENGINE_SECTION][
				READ_RES_DIR_OPTION]
		self.engineconf.debugdir = cparser[ENGINE_SECTION][
				READ_RES_DBG_DIR_OPTION]
		self.engineconf.releasedir = cparser[ENGINE_SECTION][
				READ_RES_REL_DIR_OPTION]

		self.__create_res_dir()

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
		cparser[LOGGER_SECTION] = {}
		cparser[LOGGER_SECTION][LOGFILE_OPTION] = str(LOGFILE_VALUE)
		cparser[LOGGER_SECTION][LOGDIR_OPTION] = str(LOGDIR_VALUE)
		cparser[LOGGER_SECTION][LOGTOFILE_OPTION] = str(LOGTOFILE_VALUE)
		cparser[LOGGER_SECTION][LOGTOSTDIO_OPTION] = str(LOGTOSTDIO_VALUE)
		cparser[LOGGER_SECTION][ENABLE_DEBUG_OPTION] = str(ENABLE_DEBUG_VALUE)

		# creating the engine section - call other function
		cparser[ENGINE_SECTION] = {}
		cparser[ENGINE_SECTION][READ_RES_DIR_OPTION] = str(READ_RES_DIR_VALUE)
		cparser[ENGINE_SECTION][READ_RES_DBG_DIR_OPTION] = str(
				READ_RES_DBG_DIR_VALUE)
		cparser[ENGINE_SECTION][READ_RES_REL_DIR_OPTION] = str(
				READ_RES_REL_DIR_VALUE)

		with open(self.gameconf, "w") as f:
			cparser.write(f)

		if self._enable_logger:
			self.engineconf.log_fname = LOGFILE_VALUE
			self.engineconf.log_fpath = LOGDIR_VALUE
			self.engineconf.log_fileio = True if (
					LOGTOFILE_VALUE == ENABLE) else False
			self.engineconf.log_stdio = True if (
					LOGTOSTDIO_VALUE == ENABLE) else False
			self.engineconf.log_level = DEBUG

		self.engineconf.readresdir = READ_RES_DIR_VALUE

		# write down the basic names of the debug and release directories
		self.engineconf.debugdir = READ_RES_DBG_DIR_VALUE
		self.engineconf.releasedir = READ_RES_REL_DIR_VALUE

		self.__create_res_dir()

	def __create_res_dir(self):
		'''
			@function __create_res_dir
			@date Thu, 17 Sep 2020 10:25:09 +0530
			@brief function to create the resource directories if they are not
			present
		'''
		# creating resource directory
		create_dir(self.engineconf.readresdir)
		if self._enable_logger:
			# debug mode
			create_dir("{}{}{}".format(self.engineconf.readresdir, sep,
				self.engineconf.debugdir))
		else:
			# release mode
			create_dir("{}{}{}".format(self.engineconf.readresdir, sep,
				self.engineconf.releasedir))

	def __get_conf_parser(self):
		'''
			@function __get_conf_parser
			@date Sun, 10 May 2020 01:21:07 +0530
			@brief private member function to get the config parser object
		'''
		cparser = ConfigParser()

		return cparser
