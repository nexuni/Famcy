import markdown
import Famcy
import json

class submitBtn(Famcy.FamcyInputBlock):
    """
    Represents the block to display
    paragraph. 
    """
    btn_style="default"                                  # (nexuni / default)
    
    def __init__(self, **kwargs):
        self.value = submitBtn.generate_template_content()
        super(submitBtn, self).__init__(**kwargs)
        self.init_block()

    @classmethod
    def generate_template_content(cls):
        return {
            "title": "inputBtn",
            "mandatory": False,
            "action_after_post": "clean",                       # (clean / save)
        }

    def init_block(self):
        self.body = Famcy.input()
        self.body["id"] = self.id
        self.body["className"] = "main_submit_btn"
        self.body["type"] = "submit"
        self.body["name"] = "send"

        if submitBtn.btn_style == "nexuni":
            self.body["className"] = "round_submit_btn"

    def render_inner(self):
        self.body["value"] = self.value["title"]
        
        return self.body