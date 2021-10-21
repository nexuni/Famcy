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
