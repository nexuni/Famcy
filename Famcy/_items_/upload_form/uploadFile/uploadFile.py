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

    def render_inner(self):
        
        file_type = ""
        if self.value["file_num"] == "multiple":
            file_type = " multiple"

        accept_type = ""
        for accept_file in self.value["accept_type"]:
            accept_type += accept_file + ", "
        accept_type = accept_type[:-2]

        inner_html = '''
        <div class="uploadFile file-loading" id="%s">
            <input id="%s_input" name="%s" type="file" %s>
        </div>
        <script>
        $(document).ready(function() {
            
            $("#%s_input").fileinput({
                allowedFileExtensions: %s
            });
        });
        </script>
        ''' % (self.id, self.id, self.name, file_type, self.id, json.dumps(self.value["accept_type"]))

        return inner_html
