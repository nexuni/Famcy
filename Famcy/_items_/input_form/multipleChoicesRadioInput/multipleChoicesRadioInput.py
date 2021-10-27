import markdown
import Famcy
import json

class multipleChoicesRadioInput(Famcy.FamcyInputBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = multipleChoicesRadioInput.generate_template_content()
        super(multipleChoicesRadioInput, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
                "title": "multipleChoicesRadioInput",
                "desc": "",
                "mandatory": False,
                "value": [],
                "action_after_post": "clean",                    # (clean / save)
            }

    def render_inner(self):
        temp = ""
        for list_value in self.value["value"]:
            temp += '<label class="rad-label"><input type="checkbox"' + self.extra_onclick_mult_btn + ' id="' + self.id + list_value + '" class="rad-input" name="' + self.name + '" value="' + list_value + '"><div class="rad-design"></div><div class="rad-text">' + list_value + '</div></label>'

        input_html = '<div id="' + self.id + '" class="multipleChoicesRadioInput ' + self.mandatory + '_mult"><h3>' + self.value["title"] + '</h3><p>' + self.value["desc"] + '</p><div>' + temp + '</div></div>' + self.extra_script_mult_btn

        return input_html
