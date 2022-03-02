import Famcy
import random
import time

class InitLight(Famcy.FamcyPage):
    def __init__(self):
        super(InitLight, self).__init__()

initL = InitLight()
InitLight.register("/InitLight", Famcy.APIStyle(), init_cls=initL)

class NewPage(Famcy.FamcyPage):
    def __init__(self):
        super(NewPage, self).__init__()

        # for declaration
        # ===============
        self.card_1 = self.card1()
        self.card_2 = self.card2()
        self.card_3 = self.card3()
        self.card_4 = self.card4()
        self.card_5 = self.card5()
        self.card_6 = self.card6()
        self.card_7 = self.card7()

        self.layout.addWidget(self.card_1, 0, 0, 1, 3)
        self.layout.addWidget(self.card_2, 1, 0, 1, 3)
        self.layout.addWidget(self.card_3, 2, 0, 2, 1)
        self.layout.addWidget(self.card_4, 2, 1, 1, 2)
        self.layout.addWidget(self.card_5, 3, 2, 2, 1)
        self.layout.addWidget(self.card_6, 4, 0, 1, 2)
        self.layout.addWidget(self.card_7, 3, 1)
        # ===============

        self.light_list = [{"red": "bulb_red", "yellow": "", "green": ""}, {"red": "", "yellow": "bulb_yellow", "green": ""}, {"red": "", "yellow": "", "green": "bulb_green"}]

        self.light_one = Famcy.FamcyBackgroundTask(self)
        self.light_two = Famcy.FamcyBackgroundTask(self)
        self.light_three = Famcy.FamcyBackgroundTask(self)
        self.light_four = Famcy.FamcyBackgroundTask(self)

        self.bg_task_val = 0
        self.bg_task_list = [self.light_one, self.light_two, self.light_three, self.light_four]

        
    # background task function 
    # ====================================================
    def background_thread_inner(self):
        val = random.randint(0,2)
        self.add_task_light(self.flash_light, {"status": self.light_list[val], "obj": self.bg_task_val, "light": val}, self.card_1, self.bg_task_list[self.bg_task_val], Famcy.FamcyPriority.Standard)

        if self.bg_task_val < 3:
            self.bg_task_val += 1
        else:
            self.bg_task_val = 0

        # self.light_one.associate(self.flash_light, info_dict={"status": self.light_list[val], "obj": 0, "light": val}, target=self.card_1)
        # Famcy.FamcyBackgroundQueue.add(self.light_one, Famcy.FamcyPriority.Standard)

        # val = random.randint(0,2)
        # self.light_two.associate(self.flash_light, info_dict={"status": self.light_list[val], "obj": 1, "light": val}, target=self.card_1)
        # Famcy.FamcyBackgroundQueue.add(self.light_two, Famcy.FamcyPriority.Standard)

        # val = random.randint(0,2)
        # self.light_three.associate(self.flash_light, info_dict={"status": self.light_list[val], "obj": 2, "light": val}, target=self.card_1)
        # Famcy.FamcyBackgroundQueue.add(self.light_three, Famcy.FamcyPriority.Standard)

        # val = random.randint(0,2)
        # self.light_four.associate(self.flash_light, info_dict={"status": self.light_list[val], "obj": 3, "light": val}, target=self.card_1)
        # Famcy.FamcyBackgroundQueue.add(self.light_four, Famcy.FamcyPriority.Standard)

    def flash_light(self, submission_obj, info_dict):
        self.card_1.layout.content[info_dict["obj"]][0].update({
                "title": "displayLight",
                "status": info_dict["status"],
                "light_size": "100%",
                "light": info_dict["light"]
            })

        r = 0
        y = 0
        g = 0
        for l in [self.card_1.layout.content[0][0].value["light"], self.card_1.layout.content[1][0].value["light"], self.card_1.layout.content[2][0].value["light"], self.card_1.layout.content[3][0].value["light"]]:
            if l == 0:
                r += 1
            elif l == 1:
                y += 1
            elif l == 2:
                g += 1
            else:
                r += 1
                y += 1
                g += 1

        self.card_1.title = "red: "+ str(r) +"; yellow: "+ str(y) +"; green: "+ str(g) +";"

    def init_light(self, submission_obj, info_list):
        self.flash_light(submission_obj, {"status": {"red": "bulb_red", "yellow": "bulb_yellow", "green": "bulb_green"}, "obj": 0, "light": 3})
        self.flash_light(submission_obj, {"status": {"red": "bulb_red", "yellow": "bulb_yellow", "green": "bulb_green"}, "obj": 1, "light": 3})
        self.flash_light(submission_obj, {"status": {"red": "bulb_red", "yellow": "bulb_yellow", "green": "bulb_green"}, "obj": 2, "light": 3})
        self.flash_light(submission_obj, {"status": {"red": "bulb_red", "yellow": "bulb_yellow", "green": "bulb_green"}, "obj": 3, "light": 3})

    def add_task_light(self, action, info_dict, target, task, priority):
        task.associate(action, info_dict=info_dict, target=target)
        Famcy.FamcyBackgroundQueue.add(task, priority)
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card1(self):
        _card1 = Famcy.FamcyCard()
        _card1.title = "red: 4; yellow: 4; green: 4;"

        _displayLight1 = Famcy.displayLight()
        _displayLight1.update({
                "title": "displayLight",
                "status": {"red": "bulb_red", "yellow": "bulb_yellow", "green": "bulb_green"}, 
                "light_size": "100%",
                "light": 3
            })

        _displayLight2 = Famcy.displayLight()
        _displayLight2.update({
                "title": "displayLight",
                "status": {"red": "bulb_red", "yellow": "bulb_yellow", "green": "bulb_green"}, 
                "light_size": "100%",
                "light": 3
            })

        _displayLight3 = Famcy.displayLight()
        _displayLight3.update({
                "title": "displayLight",
                "status": {"red": "bulb_red", "yellow": "bulb_yellow", "green": "bulb_green"}, 
                "light_size": "100%",
                "light": 3
            })

        _displayLight4 = Famcy.displayLight()
        _displayLight4.update({
                "title": "displayLight",
                "status": {"red": "bulb_red", "yellow": "bulb_yellow", "green": "bulb_green"}, 
                "light_size": "100%",
                "light": 3
            })
        
        _card1.layout.addWidget(_displayLight1, 0, 0)
        _card1.layout.addWidget(_displayLight2, 0, 1)
        _card1.layout.addWidget(_displayLight3, 0, 2)
        _card1.layout.addWidget(_displayLight4, 0, 3)

        self.thread_init_light = Famcy.FamcyBackgroundTask(self)
        initL.style.setAction(lambda: self.add_task_light(self.init_light, {}, _card1, self.thread_init_light, Famcy.FamcyPriority.Critical))
        initL.style.setReturnValue(indicator=True, message="add to task")

        return _card1

    def card2(self):
        _card2 = Famcy.FamcyCard()

        _displayImage = Famcy.displayImage()
        _displayImage.update({
                "title": "displayImage",
                "img_name": ["/static/image/test.jpg", "/static/image/test.jpg", "/static/image/test.jpg", "/static/image/test.jpg"],
                "img_size": ["40%", "30%", "20%", "10%"],
                "border_radius": None
            })

        _card2.layout.addWidget(_displayImage, 0, 0)

        return _card2

    def card3(self):
        _card3 = Famcy.FamcyCard()

        _displayParagraph = Famcy.displayParagraph()
        _displayParagraph.update({
                "title": "displayParagraph",
                "content": '''
                Technologies have advanced rapidly over the recent years. These new technologies help humans increase productivity to adapt to the world with a constantly growing population. Nowadays, half of the world's population lives in urban areas. It is expected that more than two-thirds will live in cities by 2050. Many modern cities, such as Singapore, have followed this trend and started incorporating new technologies to build a "Smart City." The increasing number of Internet of Things (IoT) devices also fuels smart city technologies and provides a tremendous amount of data for analysis. The Nexuni team believes the trend of smart city development resonates with our vision of developing automation solutions that enhance productivity and provide more business opportunities. Contact us and let us discuss options to bring future technology to the present.'''
            })

        _card3.layout.addWidget(_displayParagraph, 0, 0)

        return _card3

    def card4(self):
        _card4 = Famcy.FamcyCard()

        _displayParagraph = Famcy.displayParagraph()
        _displayParagraph.update({
                "title": "displayParagraph",
                "content": '''
                Technologies have advanced rapidly over the recent years. These new technologies help humans increase productivity to adapt to the world with a constantly growing population. Nowadays, half of the world's population lives in urban areas. It is expected that more than two-thirds will live in cities by 2050. Many modern cities, such as Singapore, have followed this trend and started incorporating new technologies to build a "Smart City." The increasing number of Internet of Things (IoT) devices also fuels smart city technologies and provides a tremendous amount of data for analysis. The Nexuni team believes the trend of smart city development resonates with our vision of developing automation solutions that enhance productivity and provide more business opportunities. Contact us and let us discuss options to bring future technology to the present.'''
            })

        _card4.layout.addWidget(_displayParagraph, 0, 0)

        return _card4

    def card5(self):
        _card5 = Famcy.FamcyCard()

        _displayParagraph = Famcy.displayParagraph()
        _displayParagraph.update({
                "title": "displayParagraph",
                "content": '''
                Technologies have advanced rapidly over the recent years. These new technologies help humans increase productivity to adapt to the world with a constantly growing population. Nowadays, half of the world's population lives in urban areas. It is expected that more than two-thirds will live in cities by 2050. Many modern cities, such as Singapore, have followed this trend and started incorporating new technologies to build a "Smart City." The increasing number of Internet of Things (IoT) devices also fuels smart city technologies and provides a tremendous amount of data for analysis. The Nexuni team believes the trend of smart city development resonates with our vision of developing automation solutions that enhance productivity and provide more business opportunities. Contact us and let us discuss options to bring future technology to the present.'''
            })

        _card5.layout.addWidget(_displayParagraph, 0, 0)

        return _card5

    def card6(self):
        _card6 = Famcy.FamcyCard()

        _displayParagraph = Famcy.displayParagraph()
        _displayParagraph.update({
                "title": "displayParagraph",
                "content": '''Technologies have advanced rapidly over the recent years. These new technologies help humans increase productivity to adapt to the world with a constantly growing population. Nowadays, half of the world's population lives in urban areas. It is expected that more than two-thirds will live in cities by 2050. Many modern cities, such as Singapore, have followed this trend and started incorporating new technologies to build a "Smart City." The increasing number of Internet of Things (IoT) devices also fuels smart city technologies and provides a tremendous amount of data for analysis. The Nexuni team believes the trend of smart city development resonates with our vision of developing automation solutions that enhance productivity and provide more business opportunities. Contact us and let us discuss options to bring future technology to the present.'''
            })

        _card6.layout.addWidget(_displayParagraph, 0, 0)

        return _card6

    def card7(self):
        _card7 = Famcy.FamcyCard()

        _displayImage = Famcy.displayImage()
        _displayImage.update({
                "title": "displayImage",
                "img_name": ["/static/image/test.jpg"],
                "img_size": ["100%"],
                "border_radius": "100%"
            })

        _card7.layout.addWidget(_displayImage, 0, 0)

        return _card7

    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    # ====================================================
    # ====================================================

   
NewPage.register("/newPage", Famcy.ClassicStyle(), permission_level=0, background_thread=True, background_freq=1)