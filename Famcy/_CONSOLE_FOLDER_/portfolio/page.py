import Famcy
import json

class PortfolioPage(Famcy.FamcyPage):
    def __init__(self):
        super(PortfolioPage, self).__init__("/portfolio", Famcy.PortfolioStyle(), background_thread=False)
        
        self.table_info = []

        self.card_1 = self.card1()
        self.layout.addWidget(self.card_1, 0, 0)

    def card1(self):
        card1 = Famcy.FamcyCard()
        # card1.title = "test"

        # card1.body.style += "padding: 0 10vw;"
        pic_word1 = Famcy.displayPicWord()
        pic_word1.update({
                "title": "test",
                "content": "cotent contentcotent contentcotent contentcotent contentcotent contentcotent contentcotent content",
                "img_src": "/static/image/FamcyUserProfilePic.png"
            })

        pic_word2 = Famcy.displayPicWord()
        pic_word2.update({
                "title": "test",
                "content": "cotent content",
                "img_src": "/static/image/FamcyUserProfilePic.png"
            })

        pic_word3 = Famcy.displayPicWord()
        pic_word3.update({
                "title": "test",
                "content": "cotent content",
                "img_src": "/static/image/FamcyUserProfilePic.png"
            })

        input_block1 = Famcy.inputBlockSec()
        input_block1.update({
                "title": "input_block",
                "content": "input_blockinput_blockinput_blockinput_blockinput_block",
                "img_src": "/static/image/FamcyUserProfilePic.png",
                "btn_name": "btn_name"
            })

        input_block2 = Famcy.inputBlockSec()
        input_block2.update({
                "title": "input_block",
                "content": "input_blockinput_blockinput_blockinput_blockinput_block",
                "img_src": "/static/image/FamcyUserProfilePic.png",
                "btn_name": "btn_name"
            })

        input_block3 = Famcy.inputBlockSec()
        input_block3.update({
                "title": "input_block",
                "content": "input_blockinput_blockinput_blockinput_blockinput_block",
                "img_src": "/static/image/FamcyUserProfilePic.png",
                "btn_name": "btn_name"
            })

        input_block4 = Famcy.inputBlockSec()
        input_block4.update({
                "title": "input_block",
                "content": "input_blockinput_blockinput_blockinput_blockinput_block",
                "img_src": "/static/image/FamcyUserProfilePic.png",
                "btn_name": "btn_name"
            })

        card1.layout.addWidget(pic_word1, 0, 0)
        card1.layout.addWidget(pic_word2, 0, 1)
        card1.layout.addWidget(pic_word3, 0, 2)
        card1.layout.addWidget(input_block1, 1, 0)
        card1.layout.addWidget(input_block2, 1, 1)
        card1.layout.addWidget(input_block3, 1, 2)
        card1.layout.addWidget(input_block4, 1, 3)
        return card1

page = PortfolioPage()
page.register()