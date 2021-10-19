# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session, abort, current_app, Blueprint
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user
import flask_sijax

import os
import importlib
import Famcy
import json
from Famcy._util_.file_utils import *
from Famcy._util_._fblock import FBlock
from Famcy._util_._submit_type import SubmitType
from gadgethiServerUtils.file_basics import *

# Define Famcy User
class FamcyUser(UserMixin):
    pass

__codename__ = "Xinhai"
famcy_dir = os.path.dirname(Famcy.__file__)

PACKAGE_NAME = "Famcy"
USER_DEFAULT_FOLDER = "_CONSOLE_FOLDER_/"
FamcyBlock = FBlock
login = login_user
logout = logout_user
user = FamcyUser
sijax = flask_sijax
SijaxSubmit = SubmitType

_current_user = current_user
_current_app = current_app
MainBlueprint = Blueprint('MainBlueprint', __name__)
print("===== Famcy Init Version Id ===== ", id(MainBlueprint))

VIDEO_CAMERA = {}

# extra python function and global variable when server init
# ====================================================================
# from Famcy._CONSOLE_FOLDER_._custom_python_.extra_init_function import EXTRA_ACTION, EXTRA_GLOBAL_VAR, LOGIN_VAR
# for action in EXTRA_ACTION:
#     action()

# for extra_var in EXTRA_GLOBAL_VAR:
#     globals()[extra_var["title"]] = extra_var["action"]

# for extra_login in LOGIN_VAR:
#     globals()[extra_login["title"]] = extra_login["action"]
# ====================================================================
# ====================================================================

def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = '00famcy00!2'
    app.config['user_default_folder'] = USER_DEFAULT_FOLDER
    app.config['package_name'] = PACKAGE_NAME
    app.config.update(read_config_yaml(app.config.get('user_default_folder','')+"famcy.yaml"))

    app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
    app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'

    sijax.Sijax().init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = app.config['main_url'] + "/iam/login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        # return FamcyUser.query.get(int(user_id))

        print("user_id: ", user_id)

        Famcy.LOGIN_BEFORE()

        get_str = Famcy.CLIENT_SERVER.client_get(Famcy.LOGIN_URL, Famcy.LOGIN_API, gauth=True)
        get_ind = json.loads(get_str)["indicator"]
        get_msg = json.loads(get_str)["message"]

        print("get_ind: ", get_ind)

        if get_ind:
            Famcy.LOGIN_AFTER(get_str)
            print("Famcy.user: ", Famcy.user)
            return Famcy.user
        return None

    # blueprint for non-auth routes of app
    # from Famcy._services_._main_service import main as main_blueprint

    # # blueprint for auth parts of app
    # from Famcy._services_.iam_service import iam as iam_blueprint
    # app.register_blueprint(iam_blueprint)

    # # blueprint for custom parts of app
    # from Famcy._CONSOLE_FOLDER_._custom_python_.cus_service import cus as cus_blueprint
    # app.register_blueprint(MainBlueprint)
    # app.register_blueprint(cus_blueprint)

    # Import Fblocks from default and custom folders. 
    # ------------------------------
    famcy_blocks = {
        "_fblocks_": [],
        USER_DEFAULT_FOLDER + "_custom_fblocks_": []
    }

    block_list = []
    for fblock_group in famcy_blocks.keys():
        famcy_blocks[fblock_group] = listdir_exclude(famcy_dir+"/"+fblock_group, exclude_list=[".", "_"])
        block_list.extend(famcy_blocks[fblock_group])

    # Check no repeat names
    assert len(block_list) == len(list(set(block_list)))

    for fblock_group in famcy_blocks.keys():
        for block in famcy_blocks[fblock_group]:
            fblock_group = fblock_group.replace('/', '.')
            globals()[block] = getattr(importlib.import_module(PACKAGE_NAME+"."+fblock_group+"."+block+"."+block), block)

    globals()["VideoCamera"] = getattr(importlib.import_module(PACKAGE_NAME+"."+"_fblocks_"+"."+"video_stream"+"."+"video_stream"), "VideoCamera")

    importlib.import_module(PACKAGE_NAME+"."+USER_DEFAULT_FOLDER[:-1]+".management.inventory.page")
    # TODO: need import module recursively for all pages in the console folder

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
