import Famcy
import json

class input_form(Famcy.FamcyBlock):
    """
    Represents the block to display
    input_form. 
    """
    def __init__(self, **kwargs):
        super(input_form, self).__init__(**kwargs)

    @classmethod
    def get_fblock_types(cls):
        """
        This is the class method
        that gets all different types
        of display that it possess
        """
        return ["pureInput", "urlBtn", "inputParagraph", "inputBtn", "inputPassword", "inputList", "singleChoiceRadioInput", "multipleChoicesRadioInput"]

    @classmethod
    def generate_values_content(cls, fblock_type=None):
        if fblock_type:
            # Check whether the type is valid
            assert fblock_type in cls.get_fblock_types()

            if fblock_type == "pureInput":
                return {
                    "type": "pureInput",
                    "title": "pureInput1",
                    "desc": "",
                    "input_type": "text",                               # text / number
                    "num_range": None,                               # if type == number
                    "placeholder": "",
                    "mandatory": True,
                }

            elif fblock_type == "inputParagraph":
                return {
                    "type": "inputParagraph",
                    "title": "inputParagraph1",
                    "desc": "",
                    "height": "300px",                                  # eg: ("200px")
                    "placeholder": "",
                    "mandatory": True,
                }

            elif fblock_type == "urlBtn":
                return {
                    "type": "urlBtn",
                    "title": "urlBtn1",
                    "style": "btn_style",                          # (link_style, btn_style)
                    "url": "http://127.0.0.1:5000/login",
                    "desc": "",
                    "mandatory": True,                          # this is useless
                    "button_name": "送出",                        # btn name in same section must not be same
                }

            elif fblock_type == "inputBtn":
                return {
                    "type": "inputBtn",
                    "title": "inputBtn1",
                    "desc": "",
                    "input_type": "number",
                    "num_range": None,                       # if type == number ([0, 10] / None)
                    "placeholder": "",
                    "mandatory": True,
                    "button_name": "送出",                     # btn name in same section must not be same
                }

            elif fblock_type == "inputPassword":
                return {
                    "type": "inputPassword",
                    "title": "inputPassword1",
                    "desc": "",
                    "mandatory": True,
                }
            elif fblock_type == "inputList":
                return {
                    "type": "inputList",
                    "title": "inputList1",
                    "desc": "",
                    "mandatory": True,
                    "value": ["list1", "list2", "list3"],
                    "list_selected_action": None
                }

            elif fblock_type == "singleChoiceRadioInput":
                return {
                    "type": "singleChoiceRadioInput",
                    "title": "singleChoiceRadioInput1",
                    "desc": "",
                    "mandatory": True,
                    "value": ["rad1", "rad2", "rad3"],
                }

            elif fblock_type == "multipleChoicesRadioInput":
                return {
                    "type": "multipleChoicesRadioInput",
                    "title": "multipleChoicesRadioInput1",
                    "desc": "",
                    "mandatory": True,
                    "value": ["check1", "check2", "check3"],
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
            "main_desc": "",
            "main_button_name": ["送出資料1", "送出資料2"], # btn name in same section must not be same
            "action_after_post": "save",                    # (clean / save)
            "submit_type": "update_block_html",
            "loader": False,
            "values": fblock_values,
            "js_after_func_dict": {}, 
            "js_after_func_name": "empty_func",             # extra script which add after fblock item
            "header_script": "",            # extra script which add in header section
            "before_function": [],          # python function that you want to run before page refresh
        }

    def render_html(self, context, **configs):

        for action in context["before_function"]:
            action(context, **configs)

        main_button_html = ""
        index = 0
        for main_button_str in context["main_button_name"]:
            main_button_html += '<input id="mb_' + str(index) + context["id"] +'" class="main_submit_btn" type="submit" name="send" value="' + main_button_str + '">'
            index += 1
        action = context["action"]
        input_html = "<p>" + context["main_desc"] + "</p>"
        for value in context["values"]:

            after_action = context["action_after_post"]
            extra_keyup = ""
            extra_script = ""
            extra_onclick_btn = ""
            extra_onclick_mult_btn = ""
            extra_script_btn = ""
            extra_script_mult_btn = ""
            if "save" in after_action:
                extra_keyup = ' onkeyup="saveValue(\'' + value["id"] + '\', this.value);"'
                extra_script = '<script type="text/javascript">document.getElementById("' + value["id"] + '").value = getSavedValue("' + value["id"] + '");</script>'
                extra_onclick_btn = ' onclick="saveValue(\'' + value["id"] + '\', \'' + value["id"] + '\' + this.value);"'
                extra_onclick_mult_btn = ' onclick="saveMultValue(\'' + value["id"] + '\', \'' + value["id"] + '\' + this.value);"'
                extra_script_btn = '<script type="text/javascript">if(getSavedValue("' + value["id"] + '") != ""){document.getElementById(getSavedValue("' + value["id"] + '")).checked = true;}</script>'
                extra_script_mult_btn = '<script type="text/javascript">for(var i = 0; i < getMultSavedValue("' + value["id"] + '").length; i++){document.getElementById(getMultSavedValue("' + value["id"] + '")[i]).checked = true;}</script>'

            if value["mandatory"]:
                mandatory = " required"
            else:
                mandatory = ""

            if value["type"] == "pureInput":
                addition_text = ""
                if value["input_type"] == "number" and value["num_range"]:
                    addition_text = ' min="' + str(value["num_range"][0]) + '" max="' + str(value["num_range"][1]) + '" '
                input_html += '<div class="pureInput"><label for="' + value["id"] + '">' + value["title"] + '</label><p>' + value["desc"] + '</p><input type="' + value["input_type"] + '" id="' + value["id"] + '" name="' + value["name"] + '" placeholder="' + value["placeholder"] + '"' + extra_keyup + addition_text + mandatory + '></div>' + extra_script

            elif value["type"] == "inputBtn":
                addition_text = ""
                if value["input_type"] == "number" and value["num_range"]:
                    addition_text = ' min="' + str(value["num_range"][0]) + '" max="' + str(value["num_range"][1]) + '" '
                input_html += '<div class="inputBtn"><label for="' + value["id"] + '">' + value["title"] + '</label><p>' + value["desc"] + '</p><input type="' + value["input_type"] + '" id="' + value["id"] + '" name="' + value["name"] + '" placeholder="' + value["placeholder"] + '"' + extra_keyup + addition_text + mandatory + '><input type="submit" name="send" value="' + value["button_name"] + '"></div>' + extra_script
            
            elif value["type"] == "inputPassword":
                input_html += '<div class="inputPassword"><label for="' + value["id"] + '">' + value["title"] + '</label><p>' + value["desc"] + '</p><div id="' + value["id"] + '" class="' + mandatory + '_password"></div></div>' + '<script>$(document).ready(function($) { $("#' + value["id"] + '").strength_meter({strengthMeterClass: "t_strength_meter", name: "' + value["name"] + '"})});</script>'

            elif value["type"] == "inputList":
                temp = ""
                for list_value in value["value"]:
                    temp += '<option name="' + value["name"] + '" value="' + list_value + '">' + list_value + '</option>'

                selected_action_flag = "True" if value["list_selected_action"] else "False"

                input_html += '<div id="l_' + value["id"] + '" class="inputList ' + mandatory + '_list"><h3>' + value["title"] + '</h3><p>' + value["desc"] + '</p><select after_action="' + after_action + '" selected_action="' + selected_action_flag + '"><option name="' + value["name"] + '" value="---">---</option>' + temp + '</select></div><script>generate_list("l_' + value["id"] + '", "' + context["id"] + '", "' + action + '", "' + context["target_id"] + '")</script>'

            elif value["type"] == "singleChoiceRadioInput":
                temp = ""
                for list_value in value["value"]:
                    temp += '<label class="rad-label"><input type="radio"' + extra_onclick_btn + ' id="' + value["id"] + list_value + '" class="rad-input" name="' + value["name"] + '" value="' + list_value + '"' + mandatory + '><div class="rad-design"></div><div class="rad-text">' + list_value + '</div></label>'

                input_html += '<div class="singleChoiceRadioInput"><h3>' + value["title"] + '</h3><p>' + value["desc"] + '</p><div>' + temp + '</div></div>' + extra_script_btn

            elif value["type"] == "multipleChoicesRadioInput":
                temp = ""
                for list_value in value["value"]:
                    temp += '<label class="rad-label"><input type="checkbox"' + extra_onclick_mult_btn + ' id="' + value["id"] + list_value + '" class="rad-input" name="' + value["name"] + '" value="' + list_value + '"><div class="rad-design"></div><div class="rad-text">' + list_value + '</div></label>'

                input_html += '<div class="multipleChoicesRadioInput ' + mandatory + '_mult"><h3>' + value["title"] + '</h3><p>' + value["desc"] + '</p><div>' + temp + '</div></div>' + extra_script_mult_btn

            elif value["type"] == "urlBtn":
                input_html += '<div class="urlBtn"><p class="' + value["style"] + '_p">' + value["desc"] + '</p><button type="button" class="' + value["style"] + '" onclick="window.location.href=\'' + value["url"] + '\'">' + value["button_name"] + '</button></div>'
        
            elif value["type"] == "inputParagraph":
                input_html += '<div class="inputParagraph"><label for="' + value["id"] + '">' + value["title"] + '</label><p>' + value["desc"] + '</p><textarea style="height: ' + value["height"] + ';" id="' + value["id"] + '" name="' + value["name"] + '" placeholder="' + value["placeholder"] + '"' + extra_keyup + mandatory + '></textarea></div>' + extra_script

        return """<form id="%s" method="%s" action="%s" onsubmit="return false;">%s%s</form>
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
        """ % (context["id"], context["method"], action, input_html, main_button_html, len(context["main_button_name"]), context["id"], json.dumps(context["loader"]), context["id"], context["id"], action, context["target_id"], context["js_after_func_name"], context["id"], json.dumps(context["js_after_func_dict"]))

    def extra_script(self, header_script, **configs):
        return header_script