'''
	@file dm_exception.py
	@module dm
	@author sb
	@date Fri, 08 May 2020 15:48:08 +0530
	@brief module component containing the dm custom exceptions
'''

class DebugTypeError(TypeError):
	'''
		@class DebugTypeError
		@date Fri, 08 May 2020 15:49:12 +0530
		@brief The type of value provided for setting debug is not the right
		type
	'''
	pass

class DebugValueError(ValueError):
	'''
		@class DebugValueError
		@date Fri, 08 May 2020 15:50:58 +0530
		@brief The value provided for setting debug is not the right
		type
	'''
	pass
