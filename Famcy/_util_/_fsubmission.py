import enum
import Famcy
import _ctypes

# GLOBAL HELPER
def get_fsubmission_obj(obj_id):
    """ Inverse of id() function. But only works if the object is not garbage collected"""
    return _ctypes.PyObj_FromPtr(obj_id)

class FResponse(metaclass=abc.ABCMeta):
	def __init__(self):
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

			elif info_dict["submit_type"] == "update_block_html":
				obj_response.html('#'+block_id, info_dict["inner_text"])
				obj_response.script(info_dict["extra_script"])
				obj_response.script("$('#loading_holder').css('display','none');")

			elif info_dict["submit_type"] == "update_alert":			
				inner_text, extra_script, target_alert = generate_alert(info_dict, form_id)

				block_id = target_alert if target_alert else block_id

				if info_dict["alert_position"] == "append":
					obj_response.html_append('#'+block_id, inner_text)
				else:
					obj_response.html_prepend('#'+block_id, inner_text)

				obj_response.script(extra_script)
				obj_response.script("$('#loading_holder').css('display','none');")

			elif info_dict["submit_type"] == "update_nothing":
				obj_response.script("$('#loading_holder').css('display','none');")

			elif info_dict["submit_type"] == "redirect_page":
				obj_response.redirect(url_for(info_dict["redirect_url"]))
				# obj_response.script("$('#loading_holder').css('display','none');")

			elif info_dict["submit_type"] == "redirect_page_tab":
				obj_response.redirect(url_for("main.generate_tab_page", tab=info_dict["redirect_tab"]))
				# obj_response.script("$('#loading_holder').css('display','none');")

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
		self.func = lambda *a, **k: pass
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

