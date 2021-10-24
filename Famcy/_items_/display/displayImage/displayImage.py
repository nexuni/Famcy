import markdown
import Famcy
import json

class displayImage(Famcy.FamcyBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = displayImage.generate_template_content()
        super(displayImage, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
                "title": "下面這個解析度也太糟糕了吧",
                "img_name": [],
                "img_size": []
            }

    def render_inner(self):
        temp = ""
        for img_name, img_size in zip(self.value["img_name"], self.value["img_size"]):
            temp += '<img style="width:' + img_size + ';" src="' + img_name + '">'
        inner_html = '<div id="' + self.id + '" class="displayImage"><h3>' + self.value["title"] + '</h3><div>' + temp + '</div></div>'
        return inner_html
