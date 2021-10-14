import Famcy
from flask import flash
from flask import current_app
import json

class upload_form(Famcy.FamcyBlock):
    """
    Represents the block to upload 
    all kinds of files. 
    """
    def __init__(self, **kwargs):
        super(upload_form, self).__init__(**kwargs)

    @classmethod
    def get_fblock_types(cls):
        """
        This is the class method
        that gets all different types
        of display that it possess
        """
        return ["uploadFile"]

    @classmethod
    def generate_values_content(cls, fblock_type=None):
        """
        This is the function that
        returns the template content 
        for the given fblock. 
        - Return a content dictionary
        """
        if fblock_type:
            # Check whether the type is valid
            assert fblock_type in cls.get_fblock_types()

            if fblock_type == "uploadFile":
                return {
                    "type": "uploadFile",
                    "title": "uploadFile11",
                    "file_num": "multiple",                     # ("single", "multiple")
                    "accept_type": ["png", "jpg"],
                    "file_path": '/__submissions__'
                }
                
    @classmethod
    def generate_template_content(cls, fblock_values=None):
        """
        This is the function that
        returns the template content 
        for the given fblock. 
        - Return a content dictionary
        """
        return {
            "submit_type": "update_alert",
            "loader": False,
            "main_button_name": ["送出資料1", "送出資料2"], # btn name in same section must not be same
            "values": fblock_values,
            "js_after_func_dict": {},
            "js_after_func_name": "empty_func",             # extra script which add after fblock item
            "header_script": "",            # extra script which add in header section
            "before_function": [],          # python function that you want to run before page refresh
        }

    def render_html(self, context, **configs):

        for action in context["before_function"]:
            action(context, **configs)

        style_script = """
        <link href="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.2/css/fileinput.min.css" media="all" rel="stylesheet" type="text/css" />
        <script src="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.2/js/plugins/piexif.min.js" type="text/javascript"></script>
        <script src="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.2/js/plugins/sortable.min.js" type="text/javascript"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.2/js/fileinput.min.js"></script>
        """

        main_button_html = ""
        index = 0
        for main_button_str in context["main_button_name"]:
            main_button_html += '<input id="mb_' + str(index) + context["id"] +'" class="main_submit_btn" type="submit" name="send" value="' + main_button_str + '">'
            index += 1
        action = context["action"]
        input_html = ""

        index = len(context["values"])

        for value in context["values"]:

            file_type = ""
            if value["file_num"] == "multiple":
                file_type = " multiple"

            accept_type = ""
            for accept_file in value["accept_type"]:
                accept_type += accept_file + ", "
            accept_type = accept_type[:-2]

            input_html += '''
            <div class="uploadFile file-loading">
                <input id="%s" name="%s" type="file" %s>
            </div>
            <script>
            $(document).ready(function() {
                
                $("#%s").fileinput({
                    allowedFileExtensions: %s
                });
            });
            </script>
            ''' % (value["id"], value["id"], file_type, value["id"], json.dumps(value["accept_type"]))

            
            # input_html += '<div class="uploadFile"><input class="file" data-browse-on-zone-click="true" type="file" accept="' + accept_type + '" id="' + value["id"] + '" name="' + value["name"] + '"' + file_type + '></div>'
                

        extra_script = ""

        return """%s<form id="%s" enctype="multipart/form-data" onsubmit="return false;" method="%s" action="%s">%s%s</form>%s
        <script type="text/javascript">

            $(function() {
                for(var i=0; i < %s; i++) {
                    $('#mb_' + i + '%s').bind('click', (e) => {
                        if (%s) {
                            $('#loading_holder').css("display","flex");
                        } 
                        var reader
                        var response_dict = {}
                        for (var j=0; j < %s; j++) {
                            upload_file(j, response_dict, i, [e.currentTarget.value])
                        }
                    });
                }

                function upload_file(i, response_dict, btn_index, btn_name) {
                    var file = document.getElementById("%s-" + i)
                    var reader = new FileReader();
                    var file_name = document.getElementsByClassName("file-caption-info")
                    function readFile(index) {
                        if( index >= file.files.length ) {
                            return;
                        }
                        var f = file.files[index];
                        reader.readAsDataURL(f);
                        reader.onload = function(e) {
                            response_dict["%s-" + i] = [e.target.result.split(",")[1], file_name[index].innerText, i]
                            response_dict["mb" + btn_index + "%s"] = btn_name
                            Sijax.request('update_page', ["%s", "%s", "%s", response_dict]);
                            readFile(index+1)
                        }
                    }
                    readFile(0);
                }
            });
        </script>
        <script>%s('%s', %s)</script>
        """ % (style_script, context["id"], context["method"], action, input_html, main_button_html, extra_script, len(context["main_button_name"]), context["id"], json.dumps(context["loader"]), index, context["id"], context["id"], context["id"], context["id"], action, context["target_id"], context["js_after_func_name"], context["id"], json.dumps(context["js_after_func_dict"]))

    def extra_script(self, header_script, **configs):
        return header_script
