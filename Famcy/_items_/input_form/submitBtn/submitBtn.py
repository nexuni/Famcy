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

    def set_btn_style(self, style_num=None):
        if style_num and style_num < 5:
            if style_num == 1:
                # default style
                self.body.classList.remove("round_submit_btn")

            if style_num == 2:
                # nexuni style => main color
                self.body["className"] = "round_submit_btn"
                self.body.style["background-color"] = "#E2E139"
                self.body.style["color"] = "#1A1A1A"

            if style_num == 3:
                # nexuni style => black color
                self.body["className"] = "round_submit_btn"
                self.body.style["background-color"] = "#2d2d2d"
                self.body.style["color"] = "#ffffff"

            if style_num == 4:
                # nexuni style => pink color
                self.body["className"] = "round_submit_btn"
                self.body.style["background-color"] = "#E68B47"
                self.body.style["color"] = "#ffffff"

            if style_num == 5:
                # nexuni style => blue color
                self.body["className"] = "round_submit_btn"
                self.body.style["background-color"] = "#49B0E6"
                self.body.style["color"] = "#ffffff"
                

    def render_inner(self):
        self.body["value"] = self.value["title"]
        
        return self.body