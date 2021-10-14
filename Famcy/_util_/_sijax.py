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










		
	# @staticmethod
	# @exception_handler
	# def update_tab_html(obj_response, form_id, tab_name, block_id, response_dict):
	# 	"""
	# 	info_dict = {"inner_text": [section_content_html, section_content_html], "extra_script": "console.log('succeed')"}
	# 	"""

	# 	info_dict = get_submission_info_dict(form_id, tab_name, block_id, response_dict)

	# 	inner_text = ""
	# 	for inner_html in info_dict["inner_text"]:
	# 		inner_text += """
	# 		<div class="%s">
	# 			<div class="title_holder">
	# 				<h2 class="section_title">%s</h2>
	# 			</div>
	# 			<div class="inner_section_content" id="%s">
	# 				%s
	# 			</div>
	# 		</div>
	# 		""" % (inner_html["size"], inner_html["title"], inner_html["target_id"], inner_html["content"])


	# 	obj_response.html('#content_section', inner_text)
	# 	obj_response.script(info_dict["extra_script"])
	# 	obj_response.script("$('#loading_holder').css('display','none');")

	# @staticmethod
	# @exception_handler
	# def update_block_html(obj_response, form_id, tab_name, block_id, response_dict):
	# 	"""
	# 	info_dict = {"inner_text": inner_text, "extra_script": "console.log('succeed')"}
	# 	"""

	# 	info_dict = get_submission_info_dict(form_id, tab_name, block_id, response_dict)

	# 	obj_response.html('#'+block_id, info_dict["inner_text"])
	# 	obj_response.script(info_dict["extra_script"])
	# 	obj_response.script("$('#loading_holder').css('display','none');")

	# @staticmethod
	# @exception_handler
	# def update_alert(obj_response, form_id, tab_name, block_id, response_dict):
	# 	"""
	# 	info_dict = {"alert_type":"alert-primary", "alert_message":submission_list, "alert_position":"prepend"}
	# 	alert_type => (alert-primary, alert-secondary, alert-success, alert-danger, alert-warning, alert-info, alert-light, alert-dark)
	# 	alert_position = > (append, prepend)
	# 	"""
	# 	if tab_name == "":
	# 		info_dict = response_dict

	# 	else:
	# 		info_dict = get_submission_info_dict(form_id, tab_name, block_id, response_dict)
		
	# 	inner_text, extra_script = generate_alert(info_dict, form_id)

	# 	if info_dict["alert_position"] == "append":
	# 		obj_response.html_append('#'+block_id, inner_text)
	# 	else:
	# 		obj_response.html_prepend('#'+block_id, inner_text)

	# 	obj_response.script(extra_script)
	# 	obj_response.script("$('#loading_holder').css('display','none');")

	# @staticmethod
	# @exception_handler
	# def update_nothing(obj_response, form_id, tab_name, block_id, response_dict):
	# 	info_dict = get_submission_info_dict(form_id, tab_name, block_id, response_dict)
	# 	obj_response.script("$('#loading_holder').css('display','none');")

	# @staticmethod
	# @exception_handler
	# def redirect_page(obj_response, form_id, tab_name, block_id, response_dict):
	# 	info_dict = get_submission_info_dict(form_id, tab_name, block_id, response_dict)
	# 	obj_response.redirect(url_for(info_dict["redirect_url"]))
	# 	obj_response.script("$('#loading_holder').css('display','none');")

	# @staticmethod
	# @exception_handler
	# def submit_login_section(obj_response, form_id, tab_name, block_id, response_dict):
	# 	mb_name = get_main_btn_value(response_dict)[0]

	# 	if mb_name == LOGIN_BTN_NAME:
	# 		sub_list = Famcy.put_submissions_to_list(response_dict, form_id)

	# 		email = sub_list[0][0]
	# 		password = sub_list[1][0]
	# 		remember = True if sub_list[2][0] == "是" else False

	# 		user = FamcyUser.query.filter_by(email=email).first()

	# 		# check if user actually exists
	# 		# take the user supplied password, hash it, and compare it to the hashed password in database
	# 		if not user or not check_password_hash(user.password, password):
	# 			obj_response.script("$('#loading_holder').css('display','none');")
	# 			inner_text, extra_script = generate_alert({"alert_type":"alert-danger", "alert_message":"登入失敗", "alert_position":"prepend"}, form_id)
	# 			obj_response.html_prepend('#'+block_id, inner_text)
	# 			obj_response.script(extra_script)

	# 		else:
	# 			# if the above check passes, then we know the user has the right credentials
	# 			login_user(user, remember=remember)
	# 			obj_response.script("$('#loading_holder').css('display','none');")
	# 			obj_response.redirect(url_for('main.home'))

	# @staticmethod
	# @exception_handler
	# def submit_signup_section(obj_response, form_id, tab_name, block_id, response_dict):
	# 	sub_list = Famcy.put_submissions_to_list(response_dict, form_id)
	# 	name = sub_list[0][0]
	# 	email = sub_list[1][0]
	# 	password = sub_list[2][0]

	# 	user = FamcyUser.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

	# 	if user: # if a user is found, we want to redirect back to signup page so user can try again  
	# 		obj_response.script("$('#loading_holder').css('display','none');")

	# 		inner_text, extra_script = generate_alert({"alert_type":"alert-warning", "alert_message":"此帳號已被註冊", "alert_position":"prepend"}, form_id)
	# 		obj_response.html_prepend('#'+block_id, inner_text)
	# 		obj_response.script(extra_script)
	# 	else:
	# 		profile_pic_url = current_app.config.get("default_profile_pic_url", "")

	# 		# create new user with the form data. Hash the password so plaintext version isn't saved.
	# 		new_user = FamcyUser(email=email, name=name, profile_pic_url=profile_pic_url,\
	# 			password=generate_password_hash(password, method='sha256'))

	# 		# add the new user to the database
	# 		Famcy.db.session.add(new_user)
	# 		Famcy.db.session.commit()

	# 		obj_response.script("$('#loading_holder').css('display','none');")
	# 		obj_response.redirect(url_for('iam.login'))

	# @staticmethod
	# @exception_handler
	# def submit_profile_section(obj_response, form_id, tab_name, block_id, response_dict):
	# 	mb_name = get_main_btn_value(response_dict)[0]

	# 	if mb_name == CHANGE_PROFILE_INFO_BTN_NAME:
	# 		sub_list = Famcy.put_submissions_to_list(response_dict, form_id)

	# 		name = sub_list[0][0]
	# 		email = sub_list[1][0]
	# 		password = sub_list[2][0]

	# 		user = FamcyUser.query.filter_by(email=current_user.email).first()
			
	# 		if name != "":
	# 			user.name = name
	# 		if email != "":
	# 			user.email = email
	# 		if password != "":
	# 			user.password = password

	# 		Famcy.db.session.commit()

	# 		obj_response.script("$('#loading_holder').css('display','none');")
	# 		inner_text, extra_script = generate_alert({"alert_type":"alert-warning", "alert_message":"資訊修改成功", "alert_position":"prepend"}, form_id)		
	# 		obj_response.html_prepend('#'+block_id, inner_text)
	# 		obj_response.script(extra_script)
	# 		obj_response.redirect(url_for('iam.profile_page'))

	# 	elif mb_name == CHANGE_PROFILE_PIC_BTN_NAME:
	# 		sub_list = Famcy.put_submissions_to_list(response_dict, form_id)

	# 		if sub_list[0][0] != "":
	# 			img_data = base64.b64decode(sub_list[0][0])
	# 			index = int(sub_list[0][2])
	# 			with open("./static/image/FamcyUserProfilePic." + sub_list[0][1].split(".")[1], "wb") as fh:
	# 				fh.write(img_data)

	# 			user = FamcyUser.query.filter_by(email=current_user.email).first()
	# 			user.profile_pic_url = "../static/image/FamcyUserProfilePic." + sub_list[0][1].split(".")[1]
	# 			Famcy.db.session.commit()
				
	# 			obj_response.script("$('#loading_holder').css('display','none');")
	# 			inner_text, extra_script = generate_alert({"alert_type":"alert-warning", "alert_message":"照片修改成功", "alert_position":"prepend"}, form_id)		
	# 			obj_response.html_prepend('#'+block_id, inner_text)
	# 			obj_response.script(extra_script)
	# 			obj_response.redirect(url_for('iam.profile_page'))

	# 		else:
	# 			obj_response.script("$('#loading_holder').css('display','none');")
	# 			inner_text, extra_script = generate_alert({"alert_type":"alert-warning", "alert_message":"未上傳照片", "alert_position":"prepend"}, form_id)		
	# 			obj_response.html_prepend('#'+block_id, inner_text)
	# 			obj_response.script(extra_script)

