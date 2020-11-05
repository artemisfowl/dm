'''
	@file dm_exception.py
	@module dm
	@author sb
	@date Fri, 08 May 2020 15:48:08 +0530
	@brief module component containing the dm custom exceptions
'''

class EnableLoggerTypeError(TypeError):
	'''
		@class EnableLoggerTypeError
		@date Fri, 08 May 2020 15:49:12 +0530
		@brief The type of value provided for setting debug is not the right
		type
	'''
	pass

class EnableLoggerValueError(ValueError):
	'''
		@class EnableLoggerValueError
		@date Fri, 08 May 2020 15:50:58 +0530
		@brief The value provided for setting debug is not the right
		type
	'''
	pass

class ResourceDirException(Exception):
	'''
		@class ResourceDirError
		@date Thu, 05 Nov 2020 18:32:22 +0530
		@brief Exception to be thrown when the resource directory to be
		monitored is either not present or wrong path is set
	'''
	pass
