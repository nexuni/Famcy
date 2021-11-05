import markdown
import Famcy
import json

class uploadFile(Famcy.FamcyUploadBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.value = uploadFile.generate_template_content()
        super(uploadFile, self).__init__()
        self.init_block()

    @classmethod
    def generate_template_content(cls, fblock_type=None):
        return {
            "title": "uploadFile",
            "file_num": "multiple",                     # ("single", "multiple")
            "accept_type": ["png", "jpg"],
            "file_path": '',
            "mandatory": True,
            "action_after_post": "clean",                    # (clean)
        }

    def init_block(self):
        self.body = Famcy.div()
        self.body["id"] = self.id
        self.body["className"] = "uploadFile"
        self.body["className"] = "file-loading"

        input_temp = Famcy.input()
        input_temp["id"] = self.id + "_input"
        input_temp["name"] = self.name
        input_temp["type"] = "file"

        script = Famcy.script()

        self.body.addElement(input_temp)
        self.body.addElement(script)

    def render_inner(self):
        if self.value["file_num"] == "multiple":
            self.body.children[0]["multiple"] = "multiple"
        else:
            del self.body.children[0]["multiple"]

        accept_type = ""
        for accept_file in self.value["accept_type"]:
            accept_type += accept_file + ", "
        accept_type = accept_type[:-2]

        inner_html = '''
        $(document).ready(function() {
            
            $("#%s_input").fileinput({
                allowedFileExtensions: %s
            });
        });
        ''' % (self.id, json.dumps(self.value["accept_type"]))

        self.body.children[1].innerHTML = inner_html

        return self.body.render_inner()
