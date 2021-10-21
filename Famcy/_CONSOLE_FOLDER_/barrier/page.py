import Famcy

PAGE_HEADER = {
	"title": ["Nexuni 員工後台", "Nexuni 員工後台", "Nexuni 員工後台", "Nexuni 員工後台"],
    "size": ["onethird_inner_section", "onethird_inner_section", "onethird_inner_section", "half_inner_section"],
    "type": ["display", ["display", "input_form"], ["display", "input_form"], ["display", "input_form"]]
}

style = Famcy.FamcyStyle()

class BarrierPage(Famcy.FamcyPage):
	def __init__(self):
		super(BarrierPage, self).__init__("/barrier", style)
		self.layout.addWidget()

	def card1(self):
		card1 = Famcy.FamcyCard()

		display_paragraph_value_1 = Famcy.displayParagraph.generate_template_content()
		display_paragraph_value_1.update({
			"title": "標題更新",
	    	"content": "這是什麼東西的**Update**"
		})
		block1 = Famcy.displayParagraph()
		block1.value = display_paragraph_value_1

		display_paragraph_value_2 = Famcy.displayParagraph.generate_template_content()
		block2 = Famcy.displayParagraph()
		block2.value = display_paragraph_value_2

		card1.layout.addWidget(block1, 0, 0, 1, 1)
		card1.layout.addWidget(block2, 1, 0, 1, 1)
		return card1

	def card2(self):
		card2 = Famcy.FamcyCard()

		display_paragraph_value_1 = Famcy.displayTag.generate_template_content()
		display_paragraph_value_1.update({
			"title": "不知道這是用來幹嘛的Layout???????????",
		    "content": "到底Display Tag有什麼用??????????",
		})
		block1 = Famcy.displayTag()
		block1.value = display_paragraph_value_1

		display_paragraph_value_2 = Famcy.displayParagraph.generate_template_content()
		block2 = Famcy.displayParagraph()
		block2.value = display_paragraph_value_2

		card1.layout.addWidget(block1, 0, 0, 1, 1)
		card1.layout.addWidget(block2, 1, 0, 1, 1)
		return card1



page = BarrierPage()
page.register()



display_tag_block = Famcy.display.generate_values_content("displayTag")
display_tag_block.update({
		"title": "不知道這是用來幹嘛的Layout",
	    "content": "到底Display Tag有什麼用？",
	})

display_light_block = Famcy.display.generate_values_content("displayLight")

input_form_content = Famcy.input_form.generate_template_content()
input_form_content.update({
		"main_button_name": ["送出"], # btn name in same section must not be same
		"action_after_post": "save",                    # (clean / save)
		"values": [{
                "type": "inputList",
                "title": "inputList1",
                "desc": "some description some description some description some description some description some description some description some description some description some description some description",
                "mandatory": False,
                "value": ["red", "yellow", "green"],
            }]
	})

display_gif_block = Famcy.display.generate_values_content("displayImage")
display_gif_block.update({
		"img_name": ["../../_CONSOLE_FOLDER_/_static_/image/barrier_gif_close.gif"],
        "img_size": ["100%"]
	})

input_switch_content = Famcy.input_form.generate_template_content()
input_switch_content.update({
		"main_button_name": ["送出"], # btn name in same section must not be same
		"action_after_post": "save",                    # (clean / save)
		"values": [{
                "type": "singleChoiceRadioInput",
                "title": "singleChoiceRadioInput1",
                "desc": "some description some description some description some description some description some description some description some description some description some description some description",
                "mandatory": True,
                "value": ["open", "close"],
            }]
	})

PAGE_CONTENT = [
	Famcy.display.generate_template_content([display_paragraph_block]),
	[Famcy.display.generate_template_content([display_light_block]), input_form_content],
    [Famcy.display.generate_template_content([display_gif_block]), input_switch_content],
    [Famcy.display.generate_template_content([display_gif_block]), input_switch_content]
]

# def traffic_light_submission(submission_list, **configs):
# 	submission_dict_handler = Famcy.SijaxSubmit(PAGE_CONTENT_OBJECT[1][1].context["submit_type"])

# 	if submission_list[0][0] == "yellow":
# 		display_light_block.update({
# 			"status": {"red": "", "yellow": "bulb_yellow", "green": ""},
# 	    })
# 	elif submission_list[0][0] == "green":
# 		display_light_block.update({
# 			"status": {"red": "", "yellow": "", "green": "bulb_green"},
# 	    })
# 	elif submission_list[0][0] == "red":
# 		display_light_block.update({
# 		    "status": {"red": "bulb_red", "yellow": "", "green": ""},
# 	    })

# 	PAGE_CONTENT_OBJECT[1][0].update_page_context({
# 			"values": [display_light_block]
# 		})

# 	content = submission_dict_handler.generate_block_html(PAGE_CONTENT_OBJECT[1])
# 	return submission_dict_handler.return_submit_info(msg=content, script="console.log('succeed')")

# 	# return {"inner_text": inner_text, "extra_script": "console.log('succeed')"}


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
