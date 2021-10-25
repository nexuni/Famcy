import abc
import enum
import Famcy
import _ctypes
from Famcy._responses_.UpdateAlert

# GLOBAL HELPER
def get_fsubmission_obj(obj_id):
	""" Inverse of id() function. But only works if the object is not garbage collected"""
	return _ctypes.PyObj_FromPtr(int(obj_id))

def exception_handler(func):
	def inner_function(*args, **kwargs):
		try:
			func(*args, **kwargs)
		except:
			# Arg1 is intend to be the submission id of the submission object
			fsubmission_obj = get_fsubmission_obj(args[1])
			UpdateAlert
			inner_text, extra_script = generate_alert({"alert_type":"alert-warning", "alert_message":"系統異常", "alert_position":"prepend"}, args[1])
			args[0].html_prepend('#'+args[3], inner_text)
			args[0].script(extra_script)
			args[0].script("$('#loading_holder').css('display','none');")
	return inner_function

def put_submissions_to_list(sub_dict):
    """
    This is the helper function to put the
    submission content to a list of arguments
    - Input:
        * sub_dict: submission dictionary
    """
    ordered_submission_list = []
    for key in sorted(list(sub_dict.keys())):
        ordered_submission_list.append(sub_dict[key])

    return ordered_submission_list

class FResponse(metaclass=abc.ABCMeta):
	def __init__(self, target=None):
		self.target = target
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
	def famcy_submission_handler(obj_response, fsubmission_id, info_dict):
		"""
		This is the main submission handler that handles all
		the submission traffics. 
		"""
		# Get the submission object
		fsubmission_obj = get_fsubmission_obj(fsubmission_id)
		info_list = put_submissions_to_list(info_dict)

		# Run user defined handle submission
		# Will assume all data ready at this point
		response_obj = fsubmission_obj.func(fsubmission_obj, info_list)
		response_obj.target = fsubmission_obj.target

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

