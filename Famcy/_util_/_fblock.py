# -*- coding: UTF-8 -*-
import abc
import copy
import base64
import random
import Famcy
from Famcy._util_._fwidget import FamcyWidget

class FBlock(FamcyWidget):
    """
    Represents the base class of the fblock 
    function that displays and handles
    submissions. 

    Interface:
        render_inner: render the html content
            for the block
        handle_submission: handle form submit
            action
    """
    def __init__(self):
        self.value = FBlock.generate_template_content()

    def preload(self):
        """
        This is the preload function
        that should be executed before 
        the inner render function. 
        """
        pass

    def postload(self):
        """
        After the page is rendered, 
        apply async post load function. 
        """
        pass

    # Interface methods
    # ------------------------------------
    @classmethod
    @abc.abstractmethod
    def generate_template_content(cls):
        """
        This is the function that
        returns the template content 
        for the given fblock. 
        - Return a content dictionary - values
        """
        return NotImplemented


class FInputBlock(FBlock):
    """
    This block represents the input
    fblock and possess save/dump feature
    to cookie. 
    
    * Allow:
    mandatory
    action_after_post
    """
    def __init__(self):
        super(FInputBlock, self).__init__()

        # Settings for action after post
        # ------------------------------
        after_action = self.value["action_after_post"]

        self.extra_keyup = ""
        self.extra_script = ""
        self.extra_onclick_btn = ""
        self.extra_onclick_mult_btn = ""
        self.extra_script_btn = ""
        self.extra_script_mult_btn = ""
        if "save" in after_action:
            self.extra_keyup = ' onkeyup="saveValue(\'' + self.id + '\', this.value);"'
            self.extra_script = '<script type="text/javascript">document.getElementById("' + self.id + '").value = getSavedValue("' + self.id + '");</script>'
            self.extra_onclick_btn = ' onclick="saveValue(\'' + self.id + '\', \'' + self.id + '\' + this.value);"'
            self.extra_onclick_mult_btn = ' onclick="saveMultValue(\'' + self.id + '\', \'' + self.id + '\' + this.value);"'
            self.extra_script_btn = '<script type="text/javascript">if(getSavedValue("' + self.id + '") != ""){document.getElementById(getSavedValue("' + self.id + '")).checked = true;}</script>'
            self.extra_script_mult_btn = '<script type="text/javascript">for(var i = 0; i < getMultSavedValue("' + self.id + '").length; i++){document.getElementById(getMultSavedValue("' + self.id + '")[i]).checked = true;}</script>'

        # Settings for mandatory
        # ------------------------------
        if self.value["mandatory"]:
            self.mandatory = " required"
        else:
            self.mandatory = ""
