import abc
import enum
import Famcy
import _ctypes

# GLOBAL HELPER
def get_fsubmission_obj(obj_id):
	""" Inverse of id() function. But only works if the object is not garbage collected"""
	return _ctypes.PyObj_FromPtr(obj_id)

def exception_handler(func):
	def inner_function(*args, **kwargs):
		try:
			func(*args, **kwargs)
		except:
			inner_text, extra_script = generate_alert({"alert_type":"alert-warning", "alert_message":"系統異常", "alert_position":"prepend"}, args[1])
			args[0].html_prepend('#'+args[3], inner_text)
			args[0].script(extra_script)
			args[0].script("$('#loading_holder').css('display','none');")
	return inner_function

class FResponse(metaclass=abc.ABCMeta):
	def __init__(self):
		self.info_dict = {}
		self.finish_loading_script = "$('#loading_holder').css('display','none');"

	@abc.abstractmethod
	def response(self, sijax_response):
		"""
		This is the function that gives
		response to the sijax input
		"""
		pass

class FSubmissionSijaxHandler(object):
	"""
	This is the sijax handler for
	handling the specific submission id
	and offer a response. 
	"""
	@staticmethod
	# @exception_handler
	def famcy_submission_handler(obj_response, fsubmission_id):
		"""
		This is the main submission handler that handles all
		the submission traffics. 
		"""
		# Get the submission object
		fsubmission_obj = get_fsubmission_obj(fsubmission_id)

		# Run user defined handle submission
		# Will assume all data ready at this point
		response_obj = fsubmission_obj.func(fsubmission_obj)

		# Response according to the return response
		response_obj.response(obj_response)


class FSubmission:
	"""
	This is the submission object that
	handles all the famcy submission 
	system. 

	- Rep
		* func: user defined function
		* target: the target of the submission block
		* origin: the origin widget of the submission
	"""
	def __init__(self, origin):
		self.func = lambda *a, **k: None
		self.origin = origin
		self.target = origin

	def getFormData(self):
		"""
		This is the getter method
		to get the form layout data. 
		"""
		data = getattr(self.origin.parent, "layout", None)
		assert data, "Submission origin has no data. "
		return data

