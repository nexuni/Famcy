# -*- coding: UTF-8 -*-
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session, abort, current_app, Blueprint, send_from_directory
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user
import flask_sijax

import os
import importlib
import Famcy
import json

from Famcy._util_._fmanager import *
from Famcy._util_._fauth import *
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
FamcyLogin = FLogin
FamcyPage = FPage
FamcyCard = FCard
FamcyStyle = FStyle
FamcyPermissions = FPermissions
FamcyInputBlock = FInputBlock
FamcyResponse = FResponse
FamcyPriority = FPriority

def create_app(famcy_id, production=False):
    """
    Main creation function of the famcy application. 
    Can set to different factory settings in the future. 
    """
    # Famcy Manager that manage all global vars, imports, 
    # file systems, http
    FManager = FamcyManager(famcy_id, famcy_dir, production=production)

    # Header definitions
    FManager["CUSTOM_STATIC_PATH"] = FManager.console + "_static_"

    # Sijax, submission related
    FManager["Sijax"] = flask_sijax
    # FManager["SijaxSubmit"] = SubmitType
    FManager["SijaxStaticPath"] = FManager.main + 'static/js/sijax/'
    FManager["SijaxJsonUri"] = '/static/js/sijax/json2.js'

    # User, login related init
    FManager["FamcyUser"] = FamcyUser
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

    # ------------------------
    # --- Main app start zone
    # ------------------------
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
    FManager.assign_to_global(globals(), system_items)


    # Get all sources of fresponse definitions 
    system_responses = FManager.importclassdir(FManager.main + "/_responses_", FamcyFileImportMode.name, "", 
        exclude=["_", "."], otherwise=[], recursive=True)
    FManager.assign_to_global(globals(), system_responses)

    # Get all sources of fstyle definitions 
    system_styles = FManager.importclassdir(FManager.main + "/_style_", FamcyFileImportMode.name, "", 
        exclude=["_", "."], otherwise=[], recursive=True)
    FManager.assign_to_global(globals(), system_styles)

    # Import module recursively for all pages in the console folder
    class_dir = FManager.importclassdir(FManager.console, FamcyFileImportMode.fixed, "page", recursive=True, 
            exclude=["_", "."], otherwise=None)

    # Register the main blueprint that is used in the FamcyPage
    app.register_blueprint(MainBlueprint)

    return app

# ------ above is the flask part -----------