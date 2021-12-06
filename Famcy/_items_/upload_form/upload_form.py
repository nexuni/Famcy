import Famcy
from flask import flash
from flask import current_app
import json

class upload_form(Famcy.FamcyCard):
    """
    Represents the block to upload 
    all kinds of files. 
    """
    def __init__(self, layout_mode=Famcy.FamcyLayoutMode.recommend):
        super(upload_form, self).__init__(layout_mode=layout_mode)
        self.configs["method"] = "post"
        self.init_block()

    def init_block(self):
        self.body = Famcy.form()
        self.body["id"] = self.id
        self.body["method"] = self.configs["method"]
        self.body["action"] = self.action
        self.body["enctype"] = "multipart/form-data"

    def render_inner(self):

        header_script, self.body = self.layout.render()
        if header_script not in self.header_script:
            self.header_script += header_script

        for widget, _, _, _, _ in self.layout.content:
            if widget.clickable:

                input_tag = Famcy.input()
                input_tag["type"] = "hidden"
                input_tag["name"] = "fsubmission_obj"
                input_tag["value"] = str(widget.submission_obj_key)

                self.body.addElement(input_tag)

        return self.body