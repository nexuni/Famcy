import Famcy
import json

class inputList(Famcy.FamcyInputBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self, **kwargs):
        self.value = inputList.generate_template_content()
        super(inputList, self).__init__(**kwargs)
        self.init_block()

    @classmethod
    def generate_template_content(cls):
        return {
            "title": "inputList",
            "desc": "",
            "mandatory": False,
            "value": [],
            "returnValue": [],
            "defaultValue": None,
            "action_after_post": "clean",                    # (clean / save)
        }

    def init_block(self):
        self.body = Famcy.div()
        self.body["id"] = self.id
        self.body["className"] = "inputList"

        h3_temp = Famcy.h3()
        p_temp = Famcy.p()
        div_temp = Famcy.div()
        div_temp["id"] = self.id + '_inputList'
        div_temp["className"] = "inputList_holder"
        sel_temp = Famcy.select()

        div_temp.addElement(sel_temp)

        script = Famcy.script()
        script.innerHTML = 'generate_list("' + self.id + '")'

        self.body.addElement(h3_temp)
        self.body.addElement(p_temp)
        self.body.addElement(div_temp)
        self.body.addElement(script)

    def render_inner(self):
        self.body.children[2].children[0].children = []
        if "---" not in self.value["value"]:
            self.value["value"].insert(0, "---")
            self.value["returnValue"].insert(0, "---")
        for i, list_value in enumerate(self.value["value"]):
            opt_temp = Famcy.option()
            opt_temp["name"] = self.name
            opt_temp["value"] = str(self.value["returnValue"][i]) if len(self.value["returnValue"]) == len(self.value["value"]) else str(list_value)
            opt_temp.innerHTML = str(list_value)
            self.body.children[2].children[0].addElement(opt_temp)

        if self.value["defaultValue"]:
            self.body["default_value"] = self.value["defaultValue"]
        else:
            self.body["default_value"] = "---"

        if self.value["mandatory"]:
            self.body["className"] = "required_list"
        else:
            if "required_list" in self.body.classList:
                self.body.classList.remove("required_list")

        self.body.children[0].innerHTML = self.value["title"]
        self.body.children[1].innerHTML = self.value["desc"]
        self.body.children[2].children[0]["after_action"] = self.value["action_after_post"]

        return self.body
