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
