import Famcy

class DisplayPage(Famcy.FamcyPage):
    def __init__(self):
        super(DisplayPage, self).__init__()

        # for declaration
        # ===============
        self.card_0 = self.card0()
        self.card_1 = self.card1()
        self.card_2 = self.card2()
        self.card_3 = self.card3()
        self.card_4 = self.card4()
        self.card_5 = self.card5()
        self.card_6 = self.card6()

        self.layout.addWidget(self.card_0, 0, 0, 1, 4)
        self.layout.addWidget(self.card_6, 1, 0, 1, 4)
        self.layout.addWidget(self.card_1, 2, 0, 2, 1)
        self.layout.addWidget(self.card_4, 2, 1, 2, 1)
        self.layout.addWidget(self.card_2, 2, 2)
        self.layout.addWidget(self.card_3, 2, 3)
        self.layout.addWidget(self.card_5, 3, 2, 1, 2)
        
        
    # background task function 
    # ====================================================
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card0(self):
        card0 = Famcy.FamcyCard()
        card0.title = "Documentation of display fblocks:"

        _displayParagraph1 = Famcy.displayParagraph()
        _displayParagraph1.update({
                "title": "",
                "content":  '''
###displayImage###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * img_name: ["List of image path"] <type: list [<type: str>]>
    * img_size: ["List of image width"] <type: list [<type: str>]>
    * border_radius: "Border radius (Default: None | Example: 10px)" <type: str>
'''
            })
        _displayParagraph2 = Famcy.displayParagraph()
        _displayParagraph2.update({
                "title": "",
                "content":  '''
###displayLight###
---
    Values of fblock:
    * status: {"red": "Add class to light up red light (Default: bulb_red)", "yellow": "", "green": ""} <type: dict {"red": "bulb_red", "yellow": "bulb_yellow", "green": "bulb_green"}>
    * light_size: "Width of the traffic light (Default: 100%)" <type: str>
'''
            })
        _displayParagraph3 = Famcy.displayParagraph()
        _displayParagraph3.update({
                "title": "",
                "content":  '''
###displayParagraph###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * content: "Content of fblock: Support Markdown" <type: str>
'''
            })
        _displayParagraph4 = Famcy.displayParagraph()
        _displayParagraph4.update({
                "title": "",
                "content":  '''
###displayPicWord###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * content: "Content of fblock: Support Markdown" <type: str>
    * img_src: "Image path" <type: str>
'''
            })
        _displayParagraph5 = Famcy.displayParagraph()
        _displayParagraph5.update({
                "title": "",
                "content":  '''
###displayStepLoader###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * steps: ["Title of step"] <type: list [<type: str>]>
    * steps_status: ["Status of step"] <type: list [<"complete" | "active" | "">]>
'''
            })
        _displayParagraph6 = Famcy.displayParagraph()
        _displayParagraph6.update({
                "title": "",
                "content":  '''
###displayTag###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * content: "Content of fblock" <type: str>
    
'''
            })
        
        card0.layout.addWidget(_displayParagraph1, 0, 0)
        card0.layout.addWidget(_displayParagraph2, 0, 1)
        card0.layout.addWidget(_displayParagraph3, 0, 2)
        card0.layout.addWidget(_displayParagraph4, 1, 0)
        card0.layout.addWidget(_displayParagraph5, 1, 1)
        card0.layout.addWidget(_displayParagraph6, 1, 2)


        return card0

    def card1(self):
        card1 = Famcy.FamcyCard()

        _displayImage = Famcy.displayImage()
        _displayImage.update({
                "title": "Title of displayImage",
                "img_name": ["static/image/famcylogo.png"],
                "img_size": ["100%"],
                "border_radius": None
            })

        card1.layout.addWidget(_displayImage, 0, 0)
        return card1 

    def card2(self):
        card2 = Famcy.FamcyCard()

        _displayLight = Famcy.displayLight()
        _displayLight.update({
                "status": {"red": "bulb_red", "yellow": "", "green": ""}, 
                "light_size": "100%",
            })

        card2.layout.addWidget(_displayLight, 0, 0)
        return card2
    

    def card3(self):
        card3 = Famcy.FamcyCard()

        _displayParagraph = Famcy.displayParagraph()
        _displayParagraph.update({
                "title": "Title of displayParagraph",
                "content":  "This is an example."
            })

        card3.layout.addWidget(_displayParagraph, 0, 0)
        return card3 

    def card4(self):
        card4 = Famcy.FamcyCard()

        _displayPicWord = Famcy.displayPicWord()
        _displayPicWord.update({
                "title": "Title of displayPicWord",
                "content": "This is an example.",
                "img_src": "static/image/famcylogo.png"
            })

        card4.layout.addWidget(_displayPicWord, 0, 0)
        return card4

    def card5(self):
        card5 = Famcy.FamcyCard()

        _displayStepLoader = Famcy.displayStepLoader()
        _displayStepLoader.update({
                "title": "Title of displayStepLoader",
                "steps": ["Step1", "Step2", "Step3"],
                "steps_status": ["complete", "active", ""]
            })
        
        card5.layout.addWidget(_displayStepLoader, 0, 0)
        return card5 

    def card6(self):
        card6 = Famcy.FamcyCard()

        _displayTag = Famcy.displayTag()
        _displayTag.update({
                "title": "Title of displayTag",
                "content":  "This is an example of displayTag"
            })

        card6.layout.addWidget(_displayTag, 0, 0)
        return card6
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

   
DisplayPage.register("/displayExample", Famcy.ClassicStyle(), permission_level=0, background_thread=False)