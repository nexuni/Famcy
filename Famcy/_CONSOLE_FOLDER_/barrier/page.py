import Famcy

style = Famcy.FamcyStyle()

class BarrierPage(Famcy.FamcyPage):
	def __init__(self):
		super(BarrierPage, self).__init__("/barrier", style, background_thread=True)
		self.card_1 = self.card1()
		self.card_2 = self.card2()
		self.card_3 = self.card3()
		self.card_4 = self.card3()

		self.layout.addWidget(self.card_1, 0, 0)
		self.layout.addWidget(self.card_2, 0, 1)
		self.layout.addWidget(self.card_3, 0, 2)
		self.layout.addWidget(self.card_4, 1, 0, 1, 3)

	def background_thread_inner(self, sijax_response):
		"""
		This is the inner loop of 
		the background thread. 
		"""
		r = random.randint(1, 100)
		rtype = [{"red": "", "yellow": "bulb_yellow", "green": ""},
{"red": "", "yellow": "", "green": "bulb_green"},
{"red": "bulb_red", "yellow": "", "green": ""}]

		if r > 30:
			ridx = random.randint(0, 2)
			self.background_queue.add()

	def card1(self):
		card1 = Famcy.FamcyCard()

		block1 = Famcy.displayParagraph()
		block1.update({
			"title": "標題更新",
			"content": "這是什麼東西的**Update**"
		})

		block2 = Famcy.displayParagraph()

		card1.layout.addWidget(block1, 0, 0)
		card1.layout.addWidget(block2, 1, 0)
		return card1

	def card2(self):
		card2 = Famcy.FamcyCard()

		block1 = Famcy.displayTag()
		block1.update({
			"title": "不知道這是用來幹嘛的Layout???????????",
			"content": "到底Display Tag有什麼用??????????",
		})

		block2 = Famcy.displayLight()

		# Input form zone
		# ------------------------
		input_light = Famcy.input_form()

		light_selection = Famcy.inputList()
		light_selection.update({
				"type": "inputList",
				"title": "inputList1",
				"desc": "some description some description some description some description some description some description some description some description some description some description some description",
				"mandatory": False,
				"value": ["red", "yellow", "green"],
			})
		light_selection["action_after_post"] = "save"

		submission_btn = Famcy.submitBtn()
		submission_btn.update({
			"title": "送出"
		})

		submission_btn.connect(self.traffic_light_submit, target=block2)

		input_light.layout.addWidget(light_selection, 0, 0)
		input_light.layout.addWidget(submission_btn, 1, 0)
		# -------------------------

		card2.layout.addWidget(block1, 0, 0)
		card2.layout.addWidget(block2, 1, 0)
		card2.layout.addWidget(input_light, 2, 0)
		return card2

	def card3(self):
		card3 = Famcy.FamcyCard()

		block1 = Famcy.displayImage()
		block1.update({
			"img_name": ["/asset/image/barrier_gif_close.gif"],
			"img_size": ["100%"]
		})

		# Input form zone
		# ------------------------
		input_light = Famcy.input_form()
		input_light.action = self.route

		light_selection = Famcy.singleChoiceRadioInput()
		light_selection.update({
				"type": "singleChoiceRadioInput",
				"title": "singleChoiceRadioInput1",
				"desc": "some description some description some description some description some description some description some description some description some description some description some description",
				"mandatory": True,
				"value": ["open", "close"],
			})
		light_selection["action_after_post"] = "save"

		submission_btn = Famcy.submitBtn()
		submission_btn.update({
			"title": "送出"
		})
		# submission_btn.connect(self.card3_submit, target=block1)

		input_light.layout.addWidget(light_selection, 0, 0)
		input_light.layout.addWidget(submission_btn, 1, 0)
		# -------------------------

		card3.layout.addWidget(block1, 0, 0)
		card3.layout.addWidget(input_light, 1, 0)
		return card3

	def traffic_light_submit(self, submission_obj):
		# submission_obj.origin
		submission_list = submission_obj.getFormData().content

		if submission_list[0][0] == "yellow":
			submission_obj.target.update({
				"status": {"red": "", "yellow": "bulb_yellow", "green": ""},
		    })
		elif submission_list[0][0] == "green":
			submission_obj.target.update({
				"status": {"red": "", "yellow": "", "green": "bulb_green"},
		    })
		elif submission_list[0][0] == "red":
			submission_obj.target.update({
			    "status": {"red": "bulb_red", "yellow": "", "green": ""},
		    })
		submission_obj.target.post_submission_js = "ddd"

page = BarrierPage()
page.register()

# display_tag_block = Famcy.display.generate_values_content("displayTag")
# display_tag_block.update({
# 		"title": "不知道這是用來幹嘛的Layout",
# 	    "content": "到底Display Tag有什麼用？",
# 	})

# display_light_block = Famcy.display.generate_values_content("displayLight")

# input_form_content = Famcy.input_form.generate_template_content()
# input_form_content.update({
# 		"main_button_name": ["送出"], # btn name in same section must not be same
# 		"action_after_post": "save",                    # (clean / save)
# 		"values": [{
#                 "type": "inputList",
#                 "title": "inputList1",
#                 "desc": "some description some description some description some description some description some description some description some description some description some description some description",
#                 "mandatory": False,
#                 "value": ["red", "yellow", "green"],
#             }]
# 	})

# display_gif_block = Famcy.display.generate_values_content("displayImage")
# display_gif_block.update({
# 		"img_name": ["../../_CONSOLE_FOLDER_/_static_/image/barrier_gif_close.gif"],
#         "img_size": ["100%"]
# 	})

# input_switch_content = Famcy.input_form.generate_template_content()
# input_switch_content.update({
# 		"main_button_name": ["送出"], # btn name in same section must not be same
# 		"action_after_post": "save",                    # (clean / save)
# 		"values": [{
#                 "type": "singleChoiceRadioInput",
#                 "title": "singleChoiceRadioInput1",
#                 "desc": "some description some description some description some description some description some description some description some description some description some description some description",
#                 "mandatory": True,
#                 "value": ["open", "close"],
#             }]
# 	})

# PAGE_CONTENT = [
# 	Famcy.display.generate_template_content([display_paragraph_block]),
# 	[Famcy.display.generate_template_content([display_light_block]), input_form_content],
#     [Famcy.display.generate_template_content([display_gif_block]), input_switch_content],
#     [Famcy.display.generate_template_content([display_gif_block]), input_switch_content]
# ]

def traffic_light_submission(submission_list, **configs):
	submission_dict_handler = Famcy.SijaxSubmit(PAGE_CONTENT_OBJECT[1][1].context["submit_type"])

	if submission_list[0][0] == "yellow":
		display_light_block.update({
			"status": {"red": "", "yellow": "bulb_yellow", "green": ""},
	    })
	elif submission_list[0][0] == "green":
		display_light_block.update({
			"status": {"red": "", "yellow": "", "green": "bulb_green"},
	    })
	elif submission_list[0][0] == "red":
		display_light_block.update({
		    "status": {"red": "bulb_red", "yellow": "", "green": ""},
	    })

	PAGE_CONTENT_OBJECT[1][0].update_page_context({
			"values": [display_light_block]
		})

	content = submission_dict_handler.generate_block_html(PAGE_CONTENT_OBJECT[1])
	return submission_dict_handler.return_submit_info(msg=content, script="console.log('succeed')")

	# return {"inner_text": inner_text, "extra_script": "console.log('succeed')"}


# def barrier_switch(submission_list, **configs):
# 	submission_dict_handler = Famcy.SijaxSubmit(PAGE_CONTENT_OBJECT[2][1].context["submit_type"])

# 	if submission_list[0][0] == "open":
# 		display_gif_block.update({
# 		    "img_name": ["../../_CONSOLE_FOLDER_/_static_/image/barrier_gif.gif"],
# 	    })
# 	elif submission_list[0][0] == "close":
# 		display_gif_block.update({
# 		    "img_name": ["../../_CONSOLE_FOLDER_/_static_/image/barrier_gif_close.gif"],
# 	    })

# 	PAGE_CONTENT_OBJECT[2][0].update_page_context({
# 			"values": [display_gif_block]
# 		})

# 	content = submission_dict_handler.generate_block_html(PAGE_CONTENT_OBJECT[2])
# 	return submission_dict_handler.return_submit_info(msg=content, script="console.log('succeed')")

# 	# return {"inner_text": inner_text, "extra_script": "console.log('succeed')"}


# def barrier_switch_s(submission_list, **configs):
# 	submission_dict_handler = Famcy.SijaxSubmit(PAGE_CONTENT_OBJECT[3][1].context["submit_type"])

# 	if submission_list[0][0] == "open":
# 		display_gif_block.update({
# 		    "img_name": ["../../_CONSOLE_FOLDER_/_static_/image/barrier_gif.gif"],
# 	    })
# 	elif submission_list[0][0] == "close":
# 		display_gif_block.update({
# 		    "img_name": ["../../_CONSOLE_FOLDER_/_static_/image/barrier_gif_close.gif"],
# 	    })

# 	PAGE_CONTENT_OBJECT[3][0].update_page_context({
# 			"values": [display_gif_block]
# 		})

# 	content = submission_dict_handler.generate_block_html(PAGE_CONTENT_OBJECT[3])
# 	return submission_dict_handler.return_submit_info(msg=content, script="console.log('succeed')")
	
# 	# return {"inner_text": inner_text, "extra_script": "console.log('succeed')"}



# PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT, [None, [None, traffic_light_submission], [None, barrier_switch], [None, barrier_switch_s]])
