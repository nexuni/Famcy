import markdown
import Famcy
import json

class urlBtn(Famcy.FamcyInputBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = urlBtn.generate_template_content()
        super(urlBtn, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
            "title": "urlBtn",
            "style": "btn_style",                               # (link_style, btn_style)
            "url": "",
            "desc": "",
            "mandatory": False,                                 # this is useless
            "button_name": "送出",                              # btn name in same section must not be same
            "action_after_post": "clean",                       # (clean / save)
        }

    def render_inner(self):
        input_html = '<div id="' + self.id + '" class="urlBtn"><p class="' + self.value["style"] + '_p">' + self.value["desc"] + '</p><button type="button" class="' + self.value["style"] + '" onclick="window.location.href=\'' + self.value["url"] + '\'">' + self.value["button_name"] + '</button></div>'
        return input_html
