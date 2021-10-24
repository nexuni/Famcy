# from Famcy._util_.dashboard_utils import *
from flask import current_app
import base64

class SubmitType(object):
	"""docstring for SubmitType"""
	def __init__(self, submit_type=""):
		self.submit_type = submit_type

		self.alert_setting = {"submit_type": submit_type, "alert_type":"alert-primary", "alert_message":"", "alert_position":"prepend", "target_alert": None}
		self.block_setting = {"submit_type": submit_type, "inner_text": "", "extra_script": ""}
		self.tab_setting = {"submit_type": submit_type, "inner_text": [""], "extra_script": ""}
		self.redirect_setting = {"submit_type": submit_type, "redirect_url": "main.home"}
		self.redirect_tab_setting = {"submit_type": submit_type, "redirect_tab": ""}
		self.login_setting = {"submit_type": submit_type, "flag": False}

	def return_submit_info(self, msg="", script=""):
		if self.submit_type == "update_alert":
			self.alert_setting.update({
				"alert_message":msg
			})
			return [self.alert_setting]

		elif self.submit_type == "update_block_html":
			self.block_setting.update({
				"inner_text":msg,
				"extra_script":script
			})
			return [self.block_setting]

		elif self.submit_type == "update_tab_html":
			if isinstance(msg, list):
				self.tab_setting.update({
					"inner_text":msg,
					"extra_script":script
				})
				return [self.tab_setting]
			else:
				self.tab_setting.update({
					"inner_text":[msg],
					"extra_script":script
				})
				return [self.tab_setting]

		elif self.submit_type == "redirect_page":
			self.redirect_setting.update({
				"redirect_url":msg
			})
			return [self.redirect_setting]

		elif self.submit_type == "redirect_page_tab":
			self.redirect_tab_setting.update({
				"redirect_tab":msg
			})
			return [self.redirect_tab_setting]

		else:
			return [{"submit_type": self.submit_type}]

	def generate_block_html(self, fblock):
		if isinstance(fblock, list):
			inner_text = ""
			for _ in fblock:
				inner_text += _.get_target_html(**current_app.config)
		else:
			inner_text = fblock.get_target_html(**current_app.config)

		return inner_text

	def generate_tab_html(self, tab_path):
		inner_text, _ = user_defined_contents(tab_path)

		return inner_text

	def generate_image_data(self, img_base64):
		img_data = base64.b64decode(img_base64)

		return img_data




		