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
        # self.body["onsubmit"] = "return false;"
        self.body["enctype"] = "multipart/form-data"

    def render_inner(self):

        header_script, content_render = self.layout.render()
        if header_script not in self.header_script:
            self.header_script += header_script

        self.body.innerHTML = content_render

        upload_id = []
        for item, _, _, _, _ in self.layout.content:
            if type(item).__name__ == "FUploadBlock":
                upload_id.append(item.id)

        script = Famcy.script()
        inner_html = ""
        for widget, _, _, _, _ in self.layout.content:
            if widget.clickable:
                pass
                # inner_html += """$('#%s').bind('click', (e) => {

                #     if (%s) {
                #         $('#loading_holder').css("display","flex");
                #     }

                #     var fileObj;
                #     var formData = new FormData()
                #     upload_id = %s
                #     for (var i=0; i < upload_id.length; i++) {
                #         fileObj = document.getElementById(upload_id[i]).files[0];
                #         formData.append("file", fileObj)
                #     }
                    
                #     var response_dict = {"upload": true}
                #     for (var pair of formData.entries()) {
                #         if (pair[0] !== "btSelectAll") {
                #             if (!(pair[0] in response_dict)) {
                #                 response_dict[pair[0]] = [pair[1]]
                #             }
                #             else {
                #                 response_dict[pair[0]].push(pair[1])
                #             }
                #         }
                #     }

                #     var token = document.head.querySelector("[name~=csrf-token][content]").content
                #     Sijax.uploadRequest('famcy_submission_handler', formData, ['%s', response_dict], { data: { csrf_token: token } });
                # });""" % (widget.id, json.dumps(widget.loader), json.dumps(upload_id), str(widget.submission_obj_key))

        script.innerHTML = inner_html

        return self.body.render_inner() + script.render_inner()
