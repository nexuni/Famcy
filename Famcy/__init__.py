# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session, abort, current_app, Blueprint, send_from_directory
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user
import flask_sijax

import os
import importlib
import Famcy
import json

from Famcy._util_._fmanager import *
from Famcy._util_._fuser import *
from Famcy._util_._fblock import *
from Famcy._util_._fpage import *
from Famcy._util_._fcard import *
from Famcy._util_._flayout import *
from Famcy._util_._fstyle import *
from Famcy._util_._fpermissions import *
from Famcy._util_._fthread import *
from Famcy._util_._flayout import *
from Famcy._util_._fsubmission import *

__codename__ = "Xinhai"
famcy_dir = os.path.dirname(Famcy.__file__)

# Create Imports for User usage
FamcyBlock = FBlock
FamcyPage = FPage
FamcyCard = FCard
FamcyStyle = FStyle
FamcyPermissions = FPermissions
FamcyInputBlock = FInputBlock
FamcyResponse = FResponse

# Famcy Manager that manage all global vars, imports, 
# file systems, http
FManager = FamcyManager(famcy_dir)

# Header definitions
FManager["CUSTOM_STATIC_PATH"] = FManager.console + "_static_"

# Sijax, submission related
FManager["Sijax"] = flask_sijax
FManager["SijaxSubmit"] = SubmitType
FManager["SijaxStaticPath"] = FManager.main + 'static/js/sijax/'
FManager["SijaxJsonUri"] = '/static/js/sijax/json2.js'

# User, login related init
FManager["FamcyUser"] = FManager.importclass(FManager.console + "famcy_user", "CustomFamcyUser", otherwise=FamcyUser)
FManager["LoginManager"] = LoginManager()
FManager["CurrentUser"] = current_user

# System Wide blueprints and application object
MainBlueprint = Blueprint('MainBlueprint', __name__)
FManager["MainBlueprint"] = MainBlueprint
FManager["CurrentApp"] = current_app

# Webpage related configs
FManager["ConsoleConfig"] = FManager.read(FManager.console + "/famcy.yaml")

# Init print statement, also make sure blueprint didn't change for all time
print("===== Famcy Init Version Id ===== ", id(FManager["MainBlueprint"]))

def create_app():
    """
    Main creation function of the famcy application. 
    Can set to different factory settings in the future. 
    """
    app = Flask(__name__)
    # Some sort of security here -> TODO check on this
    app.config['SECRET_KEY'] = '00famcy00!2'

    # Init Sijax
    FManager["Sijax"].Sijax().init_app(app)

    # Init login manager
    FManager["LoginManager"].login_view = FManager["ConsoleConfig"]['member_http_url']
    FManager["LoginManager"].init_app(app)
    FManager["FamcyUser"].setup_user_loader(FManager["LoginManager"])

    # Init http client
    FManager.init_http_client(**FManager["ConsoleConfig"])

    # User Static Data
    @MainBlueprint.route('/asset/<path:filename>')
    def user_custom_asset(filename):
        # Usage in template {{ url_for('user_custom_asset', filename='doday_icon.png') }}
        return send_from_directory(FManager.console + "/" + FManager.USER_STATIC_FOLDER, filename)

    # Import Fblocks from default and custom folders. 
    # ------------------------------
    # Get all sources of fblocks definitions 
    system_items = FManager.importclassdir(FManager.main + "/_items_", FamcyFileImportMode.name, "", 
        exclude=["_", "."], otherwise=[], recursive=True)
    print("system_items ", system_items)

    # Check no repeat names
    assert len(system_items) == len(list(set(system_items))), "System Fblocks definition have duplicated names"

    # Assign flocks to global
    for module in system_items:
        block = FManager.get_module_name(module)
        globals()[block] = getattr(module, block)

    # Import module recursively for all pages in the console folder
    class_dir = FManager.importclassdir(FManager.console, FamcyFileImportMode.fixed, "page", recursive=True, 
            exclude=["_", "."], otherwise=None)
    print("class_dir ", class_dir)

    # Register the main blueprint that is used in the FamcyPage
    app.register_blueprint(MainBlueprint)

    return app

# ------ above is the flask part -----------

# ------ Famcy system utility functions -------
def generate_content_obj(page_header, page_content, submission_list=None):
    """
    This is the helper function to generate the content
    object for the page. Like compiling the content
    """
    if submission_list == None:
        submission_list = []
        for _ in range(len(page_content)):
            if isinstance(page_content[_], list):
                temp = [lambda i,**c: None for __ in range(len(page_content[_]))]
                submission_list.append(temp)
            else:
                submission_list.append(None)

    ret_list = []
    for i in range(len(page_content)):

        if isinstance(page_header["type"][i], list):
            temp = []
            if submission_list == None:
                submission_list[i] = [lambda i,**c: None for _ in range(len(page_content[i]))]
            for j in range(len(page_header["type"][i])):
                temp.append(globals()[page_header["type"][i][j]](_submission_handler=submission_list[i][j], 
                    **page_content[i][j]))
            ret_list.append(temp)

        else:
            ret_list.append(globals()[page_header["type"][i]](_submission_handler=submission_list[i], 
                **page_content[i]))

    return ret_list

def put_submissions_to_list(sub_dict, submission_id):
    """
    This is the helper function to put the
    submission content to a list of arguments
    - Input:
        * sub_dict: submission dictionary
        * submission_id: id for the submission
    """
    ordered_submission_list = []
    btn_info = []
    for key in sorted(list(sub_dict.keys())):
        # Guard the button case. 
        if submission_id not in key:
            continue
        elif "mb_" in key:
            btn_info = sub_dict[key]
            continue
        ordered_submission_list.append(sub_dict[key])

    ordered_submission_list.append(btn_info)

    return ordered_submission_list

def update_object_id(content_object_list, file_path_key, action_path):
    """
    This is the helper function to update
    the object id for all contect objects
    """
    for i in range(len(content_object_list)):
        # Single fblock case
        if not isinstance(content_object_list[i], list):
            content_object_list[i].update_id(file_path_key+"-%d"%i, action_path, file_path_key+"-%d"%i)
            continue

        for j in range(len(content_object_list[i])):
            content_object_list[i][j].update_id(file_path_key+"-%d-%d"%(i, j), action_path, file_path_key+"-%d"%i)
