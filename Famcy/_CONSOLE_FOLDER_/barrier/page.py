import Famcy
import random

class VideoStream1(Famcy.FamcyPage):
	def __init__(self):
		super(VideoStream1, self).__init__("/video_1", Famcy.VideoStreamStyle("/video_1"))

v1 = VideoStream1()
v1.register()

class BarrierPage(Famcy.FamcyPage):
	def __init__(self):
		super(BarrierPage, self).__init__("/barrier", Famcy.ClassicStyle(), background_thread=True)
		self.card_1 = self.card1()
		self.card_2 = self.card2()
		self.card_3 = self.card3()
		self.card_4 = self.card3()

		self.layout.addWidget(self.card_1, 0, 0)
		self.layout.addWidget(self.card_2, 0, 1)
		self.layout.addWidget(self.card_3, 0, 2)
		self.layout.addWidget(self.card_4, 1, 0, 1, 3)

	def background_thread_inner(self):
		"""
		This is the inner loop of 
		the background thread. 
		"""
		rtype = [{"red": "", "yellow": "bulb_yellow", "green": ""},
{"red": "", "yellow": "", "green": "bulb_green"},
{"red": "bulb_red", "yellow": "", "green": ""}]

		itype = ["/asset/image/barrier_gif_close.gif", "/asset/image/barrier_gif_close.gif", "/asset/image/barrier_gif.gif"]

		def task_a_func(self, submission_obj, info_list):
			ridx = random.randint(0, 2)
			submission_obj.target.update({"status": rtype[ridx]})
			return Famcy.UpdateBlockHtml()

		def task_bc_func(self, submission_obj, info_list):
			ridx = random.randint(0, 2)
			submission_obj.target.update({"img_name": [itype[ridx]]})
			return Famcy.UpdateBlockHtml()

		task_a = Famcy.FamcyBackgroundTask(self)
		task_a.associate(task_a_func, info_dict={}, target=self.card_2.layout.content[1][0])

		task_b = Famcy.FamcyBackgroundTask(self)
		task_b.associate(task_bc_func, info_dict={}, target=self.card_3.layout.content[0][0])

		task_c = Famcy.FamcyBackgroundTask(self)
		task_c.associate(task_bc_func, info_dict={}, target=self.card_4.layout.content[0][0])

		Famcy.FamcyBackgroundQueue.add(task_a, Famcy.FamcyPriority.Standard)
		Famcy.FamcyBackgroundQueue.add(task_b, Famcy.FamcyPriority.Standard)
		Famcy.FamcyBackgroundQueue.add(task_c, Famcy.FamcyPriority.Standard)

	def card1(self):
		card1 = Famcy.FamcyCard()

		block1 = Famcy.displayParagraph()
		block1.update({
			"title": "標題更新",
			"content": "這是什麼東西的**Update**"
		})

		block2 = Famcy.displayParagraph()

		videoStream = Famcy.video_stream()
		videoStream.update({
			"rtsp_address": ["rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"],
            "video_timeout": [15],
            "holder_width": ["100%"],
            "holder_height": ["150px"],
            "img_path": ["/video_1"]
		})

		card1.layout.addWidget(block1, 0, 0)
		card1.layout.addWidget(block2, 1, 0)
		card1.layout.addWidget(videoStream, 2, 0)
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

	def traffic_light_submit(self, submission_obj, info_list):

		if info_list[0][0] == "yellow":
			submission_obj.target.update({
				"status": {"red": "", "yellow": "bulb_yellow", "green": ""},
		    })
		elif info_list[0][0] == "green":
			submission_obj.target.update({
				"status": {"red": "", "yellow": "", "green": "bulb_green"},
		    })
		elif info_list[0][0] == "red":
			submission_obj.target.update({
			    "status": {"red": "bulb_red", "yellow": "", "green": ""},
		    })

		return Famcy.UpdateBlockHtml()

page = BarrierPage()
page.register()

