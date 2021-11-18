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
        self.header_script += """
        <link href="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.2/css/fileinput.min.css" media="all" rel="stylesheet" type="text/css" />
        <script src="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.2/js/plugins/piexif.min.js" type="text/javascript"></script>
        <script src="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.2/js/plugins/sortable.min.js" type="text/javascript"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/gh/kartik-v/bootstrap-fileinput@5.2.2/js/fileinput.min.js"></script>
        """

        self.body = Famcy.form()
        self.body["id"] = self.id
        self.body["method"] = self.configs["method"]
        self.body["action"] = self.action
        self.body["onsubmit"] = "return false;"
        self.body["enctype"] = "multipart/form-data"

    def render_inner(self):

        header_script, content_render = self.layout.render()
        if header_script not in self.header_script:
            self.header_script += header_script

        self.body.innerHTML = content_render

        inner_html = ""
        upload_file_list = []
        for widget, _, _, _, _ in self.layout.content:

            if getattr(widget, "upload", None):
                upload_file_list.append(widget.id + "_input")

            if widget.clickable:
                inner_html += """$('#%s').bind('click', (e) => {

                    if (%s) {
                        $('#loading_holder').css("display","flex");
                    }

                    var reader
                    var response_dict = {}
                    var upload_file_list = %s
                    for (var i=0; i < upload_file_list.length; i++) {
                        upload_file(response_dict, upload_file_list[i], %s)
                    }

                });""" % (widget.id, json.dumps(widget.loader), json.dumps(upload_file_list), str(widget.submission_obj_key))

        inner_html += """
            function upload_file(response_dict, widget_id, submit_id) {
                var file = document.getElementById(widget_id)
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
                        var token = document.head.querySelector("[name~=csrf-token][content]").content
                        Sijax.request('famcy_submission_handler', [submit_id, response_dict], { data: { csrf_token: token } });
                        readFile(index+1)
                    }
                }
                readFile(0);
            }
        """ % (self.id)

        script = Famcy.script()
        script.innerHTML = inner_html

        return self.body.render_inner() + script.render_inner()
