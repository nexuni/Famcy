import markdown
import Famcy
import json

class inputList(Famcy.FamcyInputBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = inputList.generate_template_content()
        super(inputList, self).__init__()

    @classmethod
    def generate_template_content(cls):
        return {
            "title": "inputList",
            "desc": "",
            "mandatory": False,
            "value": [],
            "action_after_post": "clean",                    # (clean / save)
        }

    def render_inner(self):
        temp = ""
        for list_value in self.value["value"]:
            temp += '<option name="' + self.name + '" value="' + list_value + '">' + list_value + '</option>'

        inner_html = '<div id="' + self.id + '" class="inputList ' + self.mandatory + '_list"><h3>' + self.value["title"] + '</h3><p>' + self.value["desc"] + '</p><select after_action="' + self.after_action + '"><option name="' + self.name + '" value="---">---</option>' + temp + '</select></div><script>generate_list("' + self.id + '", "' + str(id(self.submission_obj)) + '")</script>'
        return inner_html
