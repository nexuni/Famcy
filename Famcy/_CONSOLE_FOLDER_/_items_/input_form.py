import Famcy

class input_form(Famcy.FamcyCard):
	def __init__(self):
		self.configs["method"] = "post"

	def render_inner(self):
		content_render = self.layout.render()
		return """<form id="%s" method="%s" action="%s" onsubmit="return false;">%s</form>
        <script type="text/javascript">
            for(var i=0; i < %s; i++) {
                $('#mb_' + i + '%s').bind('click', (e) => {
                    if (%s) {
                        $('#loading_holder').css("display","flex");
                    } 
                    var form_element = document.getElementById('%s')
                    var formData = new FormData(form_element)
                    var response_dict = {}
                    response_dict[e.currentTarget.id] = [e.currentTarget.value]
                    for (var pair of formData.entries()) {
                        if (!(pair[0] in response_dict)) {
                            response_dict[pair[0]] = [pair[1]]
                        }
                        else {
                            response_dict[pair[0]].push(pair[1])
                        }
                    }
                    var flag = checkform(form_element)
                    if (flag) {
                        Sijax.request('update_page', ["%s", "%s", "%s", response_dict]);
                    }
                    else {
                        $('#loading_holder').css("display","none");
                    }
                });
            }
        </script>
        <script>%s("%s", %s)</script>
        """ % (context["id"], context["method"], action, input_html, len(context["main_button_name"]), context["id"], json.dumps(context["loader"]), context["id"], context["id"], action, context["target_id"], context["js_after_func_name"], context["id"], json.dumps(context["js_after_func_dict"]))