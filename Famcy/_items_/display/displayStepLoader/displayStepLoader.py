import markdown
import Famcy
import json

class displayStepLoader(Famcy.FamcyBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = displayStepLoader.generate_template_content()
        super(displayStepLoader, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
                "title": "displayStepLoader",
                "steps": ["step1", "step2", "step3"],
                "steps_status": ["complete", "active", ""]                 # ("" / "complete" / "active")
            }

    def render_inner(self):
        temp = ""
        for step_title, step_status in zip(self.value["steps"], self.value["steps_status"]):
            temp += '<li class="is-' + step_status + '"><span>' + step_title + '</span></li>'
        inner_html = '<div id="' + self.id + '" class="displayStepLoader"><h3>' + self.value["title"] + '</h3><ol class="_progress-bar">' + temp + '</ol></div>'
        return inner_html
