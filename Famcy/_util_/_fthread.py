import threading

class FamcySignal:
	"""
	This is the famcy signal that is used to
	trigger particular functions / actions
	in or out of the thread. 

	Reference Implementation: 
	https://stackoverflow.com/questions/21101500/custom-pyqtsignal-implementation
	"""
	def __init__(self):
		self.__subscribers = []

	def emit(self, *args, **kwargs):
		for subs in self.__subscribers:
			subs(*args, **kwargs)

	def connect(self, func):
		self.__subscribers.append(func)  

	def disconnect(self, func):  
		try:  
			self.__subscribers.remove(func)  
		except ValueError:  
			print('Warning: function %s not removed from signal %s'%(func,self))

class FamcyThread(threading.Thread):
	"""
	Represent the famcy thread implementation. 
	Currently it's just inherit from the
	basic threading Thread class. 
	"""
	def __init__(self, *args, **kwargs):
		super(FamcyThread, self).__init__(*args, **kwargs)

