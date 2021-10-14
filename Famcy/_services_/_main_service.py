import os
import json
import urllib
import Famcy
from Famcy import sijax
from .._util_.dashboard_utils import *
from .._util_._sijax import *
from flask import Flask, g, render_template, redirect, url_for, session, flash, request, Blueprint, current_app, render_template_string, Response
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/video_feed_<index>')
def video_feed(index):
	print("video_feed")
	address = request.args.get('address')
	timeout = request.args.get('timeout')
	Famcy.VIDEO_CAMERA['video_feed_' + index] = Famcy.VideoCamera
	Famcy.VIDEO_CAMERA['video_feed_' + index].is_decoded = False
	return Response(Famcy.VIDEO_CAMERA['video_feed_' + index].create_camera_response(address, timeout), mimetype='multipart/x-mixed-replace; boundary=frame')

# Main Routing function
# -------------------------
@main.route('/')
def home():
	return redirect(url_for("main.generate_dashboard"))

@sijax.route(main, "/dashboard", methods=['GET', 'POST'])
def generate_dashboard():
	# handle dashboard submit
	if g.sijax.is_sijax_request:
		g.sijax.register_object(SijaxHandler)
		return g.sijax.process_request()

	# handle switch tab from dashboard to others
	if request.method == 'POST':
		tab_name = request.form["side_bar_btn"]
		safe_tab_name = urllib.parse.quote_plus(tab_name)
		return redirect(url_for("main.generate_tab_page", tab=safe_tab_name))

	html_header = dashboardHTMLHeader(current_app.config.get("console_title", ""), current_app.config.get("console_description", ""))
	side_bar = dashboardSideBar(current_app.config.get("side_bar_title", ""), current_app.config.get("side_bar_hierachy", {}), title_style="bxs-store", side_bar_style={"豆漿預約": "bx-coffee-togo", "豆日子商店": "bx-shopping-bag", "歷史訂單": "bx-history", "客服": "bxs-phone", "總覽": "bx-book-open"}, 
			with_login=False)
	nav_bar = dashboardNavBar("登入", os.path.join(current_app.config.get("main_url", ""), "static", "image/login.png"), 
			with_login=False)
	
	content, extra_script = user_defined_contents(current_app.config.get("main_page", {}))
	end_js = dashboardJavaScript()
	color_theme = setColorTheme(main_color=current_app.config.get("MAIN_COLOR", "#edaf00"), sub_color=current_app.config.get("SUB_COLOR", "#f0e260"))
	load_spinner = generateLoader(current_app.config.get("LOADER", "Double_Ring"))
	
	return render_template("index.html", load_spinner=load_spinner, color_theme=color_theme, html_header=html_header, side_bar=side_bar, nav_bar=nav_bar, content=content, extra_script=extra_script, end_js=end_js)

@sijax.route(main, "/dashboard/<tab>", methods=['GET', 'POST'])
@login_required
def generate_tab_page(tab):
	# Home page redirect
	if request.method == 'POST':
		if g.sijax.is_sijax_request:
			g.sijax.register_object(SijaxHandler)
			return g.sijax.process_request()

	if tab == '-':
		return redirect(url_for("main.generate_dashboard"))

	tab_name = urllib.parse.unquote(tab)

	html_header = dashboardHTMLHeader(current_app.config.get("console_title", ""), current_app.config.get("console_description", ""))
	side_bar = dashboardSideBar(current_app.config.get("side_bar_title", ""), current_app.config.get("side_bar_hierachy", {}), title_style="bxs-store", side_bar_style={"豆漿預約": "bx-coffee-togo", "豆日子商店": "bx-shopping-bag", "歷史訂單": "bx-history", "客服": "bxs-phone", "總覽": "bx-book-open"}, 
			with_login=current_app.config.get("with_login", True))
	nav_bar = dashboardNavBar(current_user.name, current_user.profile_pic_url, with_login=current_app.config.get("with_login", True))
	# nav_bar = dashboardNavBar("current_user.name", "", with_login=current_app.config.get("with_login", True))
	
	content, extra_script = user_defined_contents(tab)
	end_js = dashboardJavaScript()
	color_theme = setColorTheme(main_color=current_app.config.get("MAIN_COLOR", "#edaf00"), sub_color=current_app.config.get("SUB_COLOR", "#f0e260"))
	load_spinner = generateLoader(current_app.config.get("LOADER", "Double_Ring"))

	return render_template("index.html", load_spinner=load_spinner, color_theme=color_theme, html_header=html_header, side_bar=side_bar, nav_bar=nav_bar, content=content, extra_script=extra_script, end_js=end_js)
	
