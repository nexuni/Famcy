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

    def render_inner(self):
        self.header_script += """
        <link href="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.2/css/fileinput.min.css" media="all" rel="stylesheet" type="text/css" />
        <script src="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.2/js/plugins/piexif.min.js" type="text/javascript"></script>
        <script src="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.2/js/plugins/sortable.min.js" type="text/javascript"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.2/js/fileinput.min.js"></script>
        """

        header_script, content_render = self.layout.render()
        if header_script not in self.header_script:
            self.header_script += header_script

        inner_html = """<form id="%s" enctype="multipart/form-data" onsubmit="return false;" method="%s" action="%s">%s</form>
        """ % (self.id, self.configs["method"], self.action, content_render)

        inner_html += """<script type="text/javascript">"""

        for widget, _, _, _, _ in self.layout.content:
            if widget.clickable:
                inner_html += """$('#%s').bind('click', (e) => {

                    if (%s) {
                        $('#loading_holder').css("display","flex");
                    }

                    var reader
                    var response_dict = {}
                    upload_file(response_dict, submit_id)
                    

                });""" % (widget.id, json.dumps(widget.loader), str(id(widget.submission_obj)))

        inner_html += """
            $(function() {

                function upload_file(response_dict, submit_id) {
                    var file = document.getElementById("%s")
                    var reader = new FileReader();
                    var file_name = document.getElementsByClassName("file-caption-info")
                    function readFile(index) {
                        if( index >= file.files.length ) {
                            return;
                        }
                        var f = file.files[index];
                        reader.readAsDataURL(f);
                        reader.onload = function(e) {
                            response_dict["%s"] = [e.target.result.split(",")[1], file_name[index].innerText, i]
                            Sijax.request('famcy_submission_handler', [submit_id, response_dict], { data: { csrf_token: token } });
                            readFile(index+1)
                        }
                    }
                    readFile(0);
                }
            });
        </script>
        """ % (self.id, self.id)

        return inner_html
