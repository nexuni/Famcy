import Famcy
from .dashboard_utils import *
from flask import redirect, url_for

from gadgethiServerUtils.time_basics import *
import base64

from threading import Thread
import functools


def generate_alert(info_dict, form_id):
	inner_text = '''
	<div class="alert %s" id="alert_msg_%s" role="alert">
		%s
	</div>
	''' % (info_dict["alert_type"], form_id, info_dict["alert_message"])

	extra_script = '''
	$("#alert_msg_%s").fadeTo(2000, 500).slideUp(500, function(){
		$("#alert_msg_%s").slideUp(500);
		$("#alert_msg_%s").remove();
	});
	''' % (form_id, form_id, form_id)

	return inner_text, extra_script, info_dict["target_alert"]

def get_main_btn_value(response_dict):
	main_btn_value = ""
	for key in list(response_dict.keys()):
		if "mb" in key:
			main_btn_value = response_dict[key]
			break
	return main_btn_value

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

class SijaxHandler(object):
	"""A container class for all Sijax handlers.

	Grouping all Sijax handler functions in a class
	(or a Python module) allows them all to be registered with
	a single line of code.
	"""
	@staticmethod
	# @exception_handler
	def update_page(obj_response, form_id, tab_name, block_id, response_dict):
		if tab_name == "":
			info_list = [response_dict]
		elif "list_flag" in list(response_dict.keys()) and response_dict["list_flag"] == "True":
			info_list = get_list_selected_action(form_id, tab_name, block_id, response_dict)
		else:
			info_list = get_submission_info_dict(form_id, tab_name, block_id, response_dict)

		for info_dict in info_list:
			if info_dict["submit_type"] == "update_tab_html":
				inner_text = ""
				for inner_html in info_dict["inner_text"]:
					if inner_html["title"] == "":
						title_sec = inner_html["title"]
					else:
						title_sec = '<div class="title_holder"><h2 class="section_title">' + inner_html["title"] + '</h2></div>'
					inner_text += """
					<div class="%s">
						%s
						<div class="inner_section_content" id="%s">
							%s
						</div>
					</div>
					""" % (inner_html["size"], title_sec, inner_html["target_id"], inner_html["content"])


				obj_response.html('#content_section', inner_text)
				obj_response.script(info_dict["extra_script"])
				obj_response.script("$('#loading_holder').css('display','none');")

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

