from flask import Blueprint, render_template, redirect, url_for, request, current_app, g
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required

from Famcy import put_submissions_to_list, sijax
from Famcy._util_.iam_utils import *
from .._util_._sijax import SijaxHandler

import os

iam = Blueprint('iam', __name__)
PATH_PREFIX = "iam/"
MODULE_PREFIX = "_iam_-"

@sijax.route(iam, "/iam/<tab>", methods=['GET', 'POST'])
def iam_handling(tab):
    if request.method == 'POST':
        if g.sijax.is_sijax_request:
            g.sijax.register_object(SijaxHandler)
            return g.sijax.process_request()

    tab_name = urllib.parse.unquote(tab)

    html_header = dashboardHTMLHeader(current_app.config.get("console_title", ""), current_app.config.get("console_description", ""))
    content, extra_script = user_defined_contents(MODULE_PREFIX+tab, PATH_PREFIX)
    end_js = dashboardJavaScript()
    color_theme = setColorTheme(main_color=current_app.config.get("MAIN_COLOR", "#edaf00"), sub_color=current_app.config.get("SUB_COLOR", "#f0e260"))
    load_spinner = generateLoader(current_app.config.get("LOADER", "Double_Ring"))

    return render_template("login.html", load_spinner=load_spinner, extra_script=extra_script, color_theme=color_theme, html_header=html_header, content=content, end_js=end_js)

@iam.route('/dashboard/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))