'''
	@file base_util.py
	@module utility
	@author sb
	@date Fri, 08 May 2020 11:45:37 +0530
	@brief module component containing the basic functions
'''

# standard libs/modules
from pathlib import Path
from os import makedirs
from logging import (Formatter, getLogger, FileHandler, StreamHandler)
from collections import namedtuple
from argparse import ArgumentParser

# custom libs/modules
from .constants_util import (RES_TYPE_DIR, RES_TYPE_FILE)
from .constants_util import (ERR_TYPE, ERR_VALUE)

# internal functions
def __chkres(res_path : str, ftype : int) :
	'''
		@function __chkres
		@date Fri, 08 May 2020 11:51:43 +0530
		@brief internal function to check the existence of the resource
		specified
		@param [IN] res_path - string containing the path to the resource to be
					checked
					ftype - integer constant defining the type of the resource
		@return True if present else False
	'''
	if res_path is None:
		raise ValueError(ERR_VALUE.format("Resource path"))
	elif not isinstance(res_path, str):
		raise TypeError(ERR_TYPE.format("Resource path", "string"))

	if ftype is None:
		raise ValueError(ERR_VALUE.format("File type identifier"))
	elif not isinstance(ftype, int):
		raise TypeError(ERR_TYPE.format("File type identifier", "integer"))

	resource = Path(res_path)
	if ftype == RES_TYPE_DIR:
		return resource.is_dir()
	elif ftype == RES_TYPE_FILE:
		return resource.is_file()

def __createres(res_path : str, ftype : int):
	'''
		@function __createres
		@date Fri, 08 May 2020 12:32:18 +0530
		@brief internal function to create the resource specified
		@param [IN] res_path - string containing the path to the resource to be
					checked
					ftype - integer constant defining the type of the resource
	'''
	if res_path is None:
		raise ValueError(ERR_VALUE.format("Resource path"))
	elif not isinstance(res_path, str):
		raise TypeError(ERR_TYPE.format("Resource path", "string"))

	if ftype is None:
		raise ValueError(ERR_VALUE.format("File type identifier"))
	elif not isinstance(ftype, int):
		raise TypeError(ERR_TYPE.format("File type identifier", "integer"))

	if ftype == RES_TYPE_DIR:
		makedirs(res_path)
	elif ftype == RES_TYPE_FILE:
		f = open(res_path, 'w')
		f.close()

# exposed functions
def check_file_exists(res_path : str):
	'''
		@function check_file_exists
		@date Fri, 08 May 2020 12:27:48 +0530
		@brief function to check if the file exists
		@param [IN] res_path - string containing path to the resource
		@return True if the file is present
	'''
	return __chkres(res_path, RES_TYPE_FILE)

def check_dir_exists(res_path : str):
	'''
		@function check_dir_exists
		@date Fri, 08 May 2020 12:27:48 +0530
		@brief function to check if the dir exists
		@param [IN] res_path - string containing path to the resource
		@return True if the dir is present
	'''
	return __chkres(res_path, RES_TYPE_DIR)

def create_file(res_path : str):
	'''
		@function create_file
		@date Fri, 08 May 2020 12:48:29 +0530
		@brief function to create the required file
		@param [IN] res_path - string containing path to the resource
	'''
	if not __chkres(res_path, RES_TYPE_FILE):
		__createres(res_path, RES_TYPE_FILE)

def create_dir(res_path : str):
	'''
		@function create_dir
		@date Fri, 08 May 2020 12:51:07 +0530
		@brief function to create the required directory
		@param [IN] res_path - string containing path to the resource
	'''
	if not __chkres(res_path, RES_TYPE_DIR):
		__createres(res_path, RES_TYPE_DIR)

def setup_logger(log_fpath, log_fname, log_level, log_stdio = False,
				log_fileio = True):
	'''
		@function setup_logger
		@date Fri, 08 May 2020 15:59:34 +0530
		@brief function to set up the formatter of the logger instance and
				return the instance
		@params[IN] log_fpath : filepath of the log file
					log_fname : filename of the log file, will be appended to
					path
					log_level : Logging level - DEBUG/WARN/ERROR etc
					log_stdio : flag to show log lines in standard IO, False by
					default
					log_fileio : flag to write log lines in log file, True by
							default
		@return root_logger : logger instance
	'''
	log_fmt = Formatter("%(asctime)s : [%(threadName)-12.12s]" +
						"[%(filename)s:%(lineno)s - %(funcName)s() ]" +
									"[%(levelname)-5.5s]  %(message)s")
	root_logger = getLogger()
	fhandler = None	# file handler - writes to the file
	chandler = None # console handler - writes to the stdio

	# setting up the file handler
	fhandler = FileHandler("{0}/{1}".format(log_fpath, log_fname))
	fhandler.setFormatter(log_fmt)

	# setting up the console handler
	chandler = StreamHandler()
	chandler.setFormatter(log_fmt)

	if log_fileio:
		root_logger.addHandler(fhandler)
	if log_stdio:
		root_logger.addHandler(chandler)

	root_logger.setLevel(log_level)

	return root_logger

def parse_args(struct_engine_mode : namedtuple):
	'''
		@function parse_args
		@date Sun, 10 May 2020 12:21:57 +0530
		@brief function to parse the arguments provided for engine
		@param [IN] struct_engine_mode - namedtuple containing the fields to be
		parsed from the arguments and populated
	'''
	if struct_engine_mode is None:
		raise ValueError(ERR_VALUE.format("Engine mode structure"))

	argsp = ArgumentParser()

	# elements handled in engine_mode_t -> struct_engine_mode
	# gameconf, build_mode

	# required arguments
	build_mode_info = "Engine mode has to be in debug(1)/release(0) - required"
	argsp.add_argument("--build-mode", help = build_mode_info, type = int)

	# optional arguments
	# NOTE : if the configuration file is not specified, a default
	# configuration file will be created
	gameconf_info = "Custom configuration filepath[absolute] - optional args"
	argsp.add_argument("--config", help = gameconf_info)

	pr = argsp.parse_args()
	struct_engine_mode.build_mode = True if (pr.build_mode == 1) else False
	struct_engine_mode.gameconf = pr.config
