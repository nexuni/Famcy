import Famcy
import os
import json
import requests
import urllib
import time

class InputPage(Famcy.FamcyPage):
    def __init__(self):
        super(InputPage, self).__init__()

        # for declaration
        # ===============
        self.pcard_1 = self.pcard1()
        self.pcard_2 = self.pcard2()

        self.layout.addStaticWidget(self.pcard_1)
        self.layout.addStaticWidget(self.pcard_2)

        self.card_0 = self.card0()
        self.card_1 = self.card1()
        self.card_2 = self.card2()
        self.card_3 = self.card3()

        self.layout.addWidget(self.card_0, 0, 0, 1, 3)
        self.layout.addWidget(self.card_1, 1, 0)
        self.layout.addWidget(self.card_2, 1, 1)
        self.layout.addWidget(self.card_3, 1, 2)
        
    # background task function 
    # ====================================================
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card0(self):
        card0 = Famcy.FamcyCard()
        card0.title = "Documentation of input fblocks:"

        _displayParagraph0 = Famcy.displayParagraph()
        _displayParagraph0.update({
                "title": "",
                "content":  '''
###Feature###
---
    Submission in Famcy:
    * input_form <parent: Famcy.FamcyCard>: Add all fblocks in input_form to do submission
    * Connect function to handle post request
        _fblock.connect(<connect after post function>)
    * After post function must contain parameter (submission_obj, user_input_data)
    * Input data can be called in list or dict
        _fblock.set_submit_value_name("<key in dict, default key is _fblock.name>")
    * Return a Famcy response in after post function

    Response in Famcy:
    * RedirectPage(redirect_url="", target=None)
    * RedirectPageTab(redirect_tab="", target=None)
    * UpdateAlert(alert_type="alert-primary", alert_message="", alert_position="prepend", extra_script=None, target=None)
    * UpdateBlockHtml(extra_script=None, target=None, upload_flag=False)
    * UpdateNothing(target=None)
    * UpdatePrompt(extra_script=None, target=None, upload_flag=False)
    * UpdateRemoveElement(prompt_flag=False, extra_script=None, target=None)
    * UpdateTabHtml(extra_script=None, target=None, upload_flag=False)

'''
            })

        _displayParagraph1 = Famcy.displayParagraph()
        _displayParagraph1.update({
                "title": "",
                "content":  '''
###inputBlockSec###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * content: "This is an example" <type: str>
    * img_src: "Image path" <type: str>
    * btn_name: "Name of submit button" <type: str>
'''
            })
        _displayParagraph2 = Famcy.displayParagraph()
        _displayParagraph2.update({
                "title": "",
                "content":  '''
###inputPassword###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * desc: "This is an example" <type: str>
    * mandatory: <Mandatory of the submission> <type: boolen>
'''
            })
        _displayParagraph3 = Famcy.displayParagraph()
        _displayParagraph3.update({
                "title": "",
                "content":  '''
###urlBtn###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * desc: "This is an example" <type: str>
    * button_name: "Name of submit button" <type: str>
    * url: "Http path of target endpoint" <type: str>
    * style: "Css style of urlBtn" <type: str ("link_style" | "btn_style")>
'''
            })
        _displayParagraph4 = Famcy.displayParagraph()
        _displayParagraph4.update({
                "title": "",
                "content":  '''
###pureInput###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * desc: "This is an example" <type: str>
    * defaultValue: "This is an example of defaultValue" <type: str>
    * input_type: "Input data type" <type: str ("text" | "number" | "password")>
    * num_range: <The range of number allowed to input> (Default: None | Example: [0, 10]) <type list [<type: int>, <type: int>]>
    * placeholder: "This is an example of placeholder" <type: str>
    * mandatory: <Mandatory of the submission> <type: boolen>
    * action_after_post: "Save data after submission" <type: str ("save", "clean")>
'''
            })
        _displayParagraph5 = Famcy.displayParagraph()
        _displayParagraph5.update({
                "title": "",
                "content":  '''
###inputBtn###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * desc: "This is an example" <type: str>
    * input_type: "Input data type" <type: str ("text" | "number" | "password")>
    * num_range: <The range of number allowed to input> (Default: None | Example: [0, 10]) <type list [<type: int>, <type: int>]>
    * placeholder: "This is an example of placeholder" <type: str>
    * button_name: "Name of submit button" <type: str>
    * mandatory: <Mandatory of the submission> <type: boolen>
    * action_after_post: "Save data after submission" <type: str ("save", "clean")>
'''
            })
        _displayParagraph6 = Famcy.displayParagraph()
        _displayParagraph6.update({
                "title": "",
                "content":  '''
###inputList###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * desc: "This is an example" <type: str>
    * value: ["Options of list"] <type: list [<type: str>]>
    * defaultValue: "This is an example of defaultValue | default: None" <type: str>
    * mandatory: <Mandatory of the submission> <type: boolen>
    * action_after_post: "Save data after submission" <type: str ("save", "clean")>
'''
            })
        _displayParagraph7 = Famcy.displayParagraph()
        _displayParagraph7.update({
                "title": "",
                "content":  '''
###inputParagraph###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * desc: "This is an example" <type: str>
    * height: "Height of input block (Default: "10vh")" <type: str>
    * placeholder: "This is an example of placeholder" <type: str>
    * mandatory: <Mandatory of the submission> <type: boolen>
    * action_after_post: "Save data after submission" <type: str ("save", "clean")>
'''
            })
        _displayParagraph8 = Famcy.displayParagraph()
        _displayParagraph8.update({
                "title": "",
                "content":  '''
###multipleChoicesRadioInput###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * desc: "This is an example" <type: str>
    * value: ["Content of options"] <type: list [<type: str>]>
    * mandatory: <Mandatory of the submission> <type: boolen>
    * action_after_post: "Save data after submission" <type: str ("save", "clean")>
'''
            })
        _displayParagraph9 = Famcy.displayParagraph()
        _displayParagraph9.update({
                "title": "",
                "content":  '''
###singleChoiceRadioInput###
---
    Values of fblock:
    * title: "Title of fblock" <type: str>
    * desc: "This is an example" <type: str>
    * value: ["Content of options"] <type: list [<type: str>]>
    * mandatory: <Mandatory of the submission> <type: boolen>
    * action_after_post: "Save data after submission" <type: str ("save", "clean")>
'''
            })
        _displayParagraph10 = Famcy.displayParagraph()
        _displayParagraph10.update({
                "title": "",
                "content":  '''
###submitBtn###
---
    Values of fblock:
    * title: "Name of submit button" <type: str>
'''
            })
        
        card0.layout.addWidget(_displayParagraph0, 0, 0, 1, 3)
        card0.layout.addWidget(_displayParagraph1, 1, 0)
        card0.layout.addWidget(_displayParagraph2, 1, 1)
        card0.layout.addWidget(_displayParagraph3, 1, 2)
        card0.layout.addWidget(_displayParagraph4, 2, 0)
        card0.layout.addWidget(_displayParagraph5, 2, 1)
        card0.layout.addWidget(_displayParagraph6, 2, 2)
        card0.layout.addWidget(_displayParagraph7, 3, 0)
        card0.layout.addWidget(_displayParagraph8, 3, 1)
        card0.layout.addWidget(_displayParagraph9, 3, 2)
        card0.layout.addWidget(_displayParagraph10, 4, 0)


        return card0

    def card1(self):
        card1 = Famcy.FamcyCard()
        card1.fit_content = True
        card1.title = "This is an example of UpdatePrompt response"

        _input_form = Famcy.input_form()

        _inputBlockSec = Famcy.inputBlockSec()
        _inputBlockSec.update({
                "title": "Title of inputBlockSec",
                "content": "Display image on prompt card",
                "img_src": "static/image/famcydark.png",
                "btn_name": "Submit inputBlockSec",
            })
        _inputBlockSec.connect(self.inputBlockSec_submit)

        _inputBtn = Famcy.inputBtn()
        _inputBtn.update({
                "title": "Title of inputBtn",
                "desc": "Display input value on prompt card",
                "input_type": "text",
                "num_range": None,
                "placeholder": "This is an example of placeholder",
                "button_name": "Submit",
                "mandatory": False,
                "action_after_post": "clean"
            })
        _inputBtn.set_submit_value_name("inputBtn_submit")
        _inputBtn.connect(self.inputBtn_submit)

        _urlBtn = Famcy.urlBtn()
        _urlBtn.update({
                "title": "Title of urlBtn",
                "style": "link_style",
                "url": "https://github.com/nexuni/Famcy",
                "desc": "This is an example",
                "button_name": "Redirect to Famcy github"
            })

        _input_form.layout.addWidget(_inputBlockSec, 0, 0)
        _input_form.layout.addWidget(_inputBtn, 1, 0)
        _input_form.layout.addWidget(_urlBtn, 2, 0)

        card1.layout.addWidget(_input_form, 0, 0)

        return card1 

    def card2(self):
        card2 = Famcy.FamcyCard()
        card2.fit_content = True
        card2.title = "This is an example of UpdateBlockHtml response"

        _input_form = Famcy.input_form()

        _pureInput = Famcy.pureInput()
        _pureInput.update({
                "title": "Title of pureInput",
                "desc": "This is an example",
                "defaultValue": "This is default input",
                "input_type": "text",
                "num_range": None,
                "placeholder": "",
                "mandatory": True,
                "action_after_post": "save",
            })

        _inputPassword = Famcy.inputPassword()
        _inputPassword.update({
                "title": "Title of inputPassword",
                "desc": "This is an example",
                "mandatory": True,
                "action_after_post": "clean",
            })

        _inputList = Famcy.inputList()
        _inputList.update({
                "title": "Title of inputList",
                "desc": "This is an example",
                "value": ["Option 1", "Option 2", "Option 3"],
                "defaultValue": None,
                "mandatory": True,
                "action_after_post": "save"
            })

        _inputParagraph = Famcy.inputParagraph()
        _inputParagraph.update({
                "title": "Title of inputParagraph",
                "desc": "This is an example",
                "height": "10vh",
                "placeholder": "This is an example of placeholder",
                "mandatory": True,
                "action_after_post": "save",
            })

        _submitBtn = Famcy.submitBtn()
        _submitBtn.update({
                "title": "Submit all info",
            })
        _submitBtn.connect(self.inputInfo_submit)

        _displayParagraph = Famcy.displayParagraph()
        _displayParagraph.update({
                "title": "",
                "content": ""
            })

        _input_form.layout.addWidget(_pureInput, 0, 0)
        _input_form.layout.addWidget(_inputPassword, 1, 0)
        _input_form.layout.addWidget(_inputList, 2, 0)
        _input_form.layout.addWidget(_inputParagraph, 3, 0)
        _input_form.layout.addWidget(_submitBtn, 4, 0)

        card2.layout.addWidget(_input_form, 0, 0)
        card2.layout.addWidget(_displayParagraph, 1, 0)

        return card2
    

    def card3(self):
        card3 = Famcy.FamcyCard()
        card3.fit_content = True
        card3.title = "This is an example of UpdateAlert response"

        _input_form = Famcy.input_form()

        _singleChoiceRadioInput = Famcy.singleChoiceRadioInput()
        _singleChoiceRadioInput.update({
                "title": "Title of singleChoiceRadioInput",
                "desc": "Please select the number that you want to sum up",
                "mandatory": False,
                "value": ["1", "2", "3"],
                "action_after_post": "clean",
            })
        _singleChoiceRadioInput.set_submit_value_name("singleChoiceRadioInput_submit")

        _multipleChoicesRadioInput = Famcy.multipleChoicesRadioInput()
        _multipleChoicesRadioInput.update({
                "title": "Title of multipleChoicesRadioInput",
                "desc": "Please select the number that you want to sum up",
                "mandatory": False,
                "value": ["1", "2", "3"],
                "action_after_post": "clean",
            })
        _multipleChoicesRadioInput.set_submit_value_name("multipleChoicesRadioInput_submit")

        _submitBtn = Famcy.submitBtn()
        _submitBtn.update({
                "title": "Sum up all numbers"
            })
        _submitBtn.connect(self.sum_up_selected_value)

        _input_form.layout.addWidget(_singleChoiceRadioInput, 0, 0)
        _input_form.layout.addWidget(_multipleChoicesRadioInput, 1, 0)
        _input_form.layout.addWidget(_submitBtn, 2, 0)

        card3.layout.addWidget(_input_form, 0, 0)

        return card3
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    def pcard1(self):
        pcard1 = Famcy.FPromptCard()

        _displayParagraph = Famcy.displayParagraph()
        _displayParagraph.update({
                "title": "The value that you entered",
                "content":  "None"
            })

        _input_form = Famcy.input_form()

        _submitBtn = Famcy.submitBtn()
        _submitBtn.update({
                "title": "Close prompt card"
            })
        _submitBtn.connect(self.remove_pcard)

        _input_form.layout.addWidget(_submitBtn, 0, 0)

        pcard1.layout.addWidget(_displayParagraph, 0, 0)
        pcard1.layout.addWidget(_input_form, 1, 0)

        return pcard1

    def pcard2(self):
        pcard2 = Famcy.FPromptCard()

        _displayImage = Famcy.displayImage()
        _displayImage.update({
                "title": "This is an example",
                "img_name": ["static/image/famcylogo.png"],
                "img_size": ["50%"],
                "border_radius": None
            })

        _input_form = Famcy.input_form()

        _submitBtn = Famcy.submitBtn()
        _submitBtn.update({
                "title": "Close prompt card"
            })
        _submitBtn.connect(self.remove_pcard)

        _input_form.layout.addWidget(_submitBtn, 0, 0)

        pcard2.layout.addWidget(_displayImage, 0, 0)
        pcard2.layout.addWidget(_input_form, 1, 0)
        return pcard2
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def remove_pcard(self, submission_obj, info_list):
        return Famcy.UpdateRemoveElement(prompt_flag=True)

    def inputBtn_submit(self, submission_obj, info_list):
        self.pcard_1.layout.content[0][0].update({
                "content":  "Return value in list: " + str(info_list[0][0]) + "; Return value in dict: " + str(info_list["inputBtn_submit"])
            })

        return Famcy.UpdatePrompt(target=self.pcard_1)

    def inputBlockSec_submit(self, submission_obj, info_list):
        return Famcy.UpdatePrompt(target=self.pcard_2)

    def inputInfo_submit(self, submission_obj, info_list):
        self.card_2.layout.content[1][0].update({
                "title": "Input information",
                "content": "pureInput: " + info_list[0][0] + "</br>inputPassword: " + info_list[1][0] + "</br>inputList: " + info_list[2][0] + "</br>inputParagraph: " + info_list[3][0]
            })
        return Famcy.UpdateBlockHtml(target=self.card_2)

    def sum_up_selected_value(self, submission_obj, info_list):
        s_submit_value = info_list["singleChoiceRadioInput_submit"] if info_list["singleChoiceRadioInput_submit"] else 0
        m_submit_value = info_list["multipleChoicesRadioInput_submit"] if info_list["multipleChoicesRadioInput_submit"] else []
        submit_sum = int(s_submit_value) + sum([int(val) for val in m_submit_value])
        msg = "The sum of values that you selected is " + str(submit_sum)
        return Famcy.UpdateAlert(target=self.card_3, alert_message=msg)
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    # ====================================================
    # ====================================================

   
InputPage.register("/inputExample", Famcy.ClassicStyle(), permission_level=0, background_thread=False)