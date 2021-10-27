import markdown
import Famcy
import json

class submitBtn(Famcy.FamcyInputBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = submitBtn.generate_template_content()
        super(submitBtn, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
            "title": "inputBtn",
            "mandatory": False,
            "action_after_post": "clean",                    # (clean / save)
        }

    def render_inner(self):
        inner_html = '<input id="' + self.id + '" class="main_submit_btn" type="submit" name="send" value="' + self.value["title"] + '">'
        return inner_html
