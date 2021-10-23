# import Famcy
import os
from flask import render_template
# from dashboard_utils import *

class FamcyStyle:

	def __init__(self, path, styleName="default", with_login=False):
		self.path = path
		self.styleName = styleName				# ("default" / "login")
		self.withLogin = with_login

		# set default value
		self.title = ""
		self.desc = ""
		self.main_color = "#3968F7"
		self.sub_color = "#94D4ED"
		self.dark_color = "#2d2d2d"
		self.white_color = "#ffffff"
		self.light_grey_color = "#f1f1f1"
		self.semi_grey_color = "#cccccc"
		self.side_bar_title = ""
		self.side_bar_hierarchy = []
		self.title_style = "bx-game"
		self.side_bar_style = {}
		self.userName = "admin"
		self.userImg = os.path.join("", "static", "image/login.png")
		self.loaderType = "Spinner"

		# default url
		self.main_url = current_app.config.get("main_url", "")

		self._check_rep()

	def _check_rep(self):
		"""
		Rep Invariant
		"""
		pass

	def setPath(self, path):
		self.path = path

	def setStyleName(self, style_name):
		self.styleName = style_name

	def setLogin(self, with_login):
		self.withLogin = with_login

	def setHeadScript(self, title=None, desc=None):
		if title:
			self.title = title
		if desc:
			self.desc = desc

	def setColor(self, main_color=None, sub_color=None, dark_color=None, white_color=None, light_grey_color=None, semi_grey_color=None):
		if main_color:
			self.main_color = main_color
		if sub_color:
			self.sub_color = sub_color
		if dark_color:
			self.dark_color = dark_color
		if white_color:
			self.white_color = white_color
		if light_grey_color:
			self.light_grey_color = light_grey_color
		if semi_grey_color:
			self.semi_grey_color = semi_grey_color

	def setSideBarInfo(self, side_bar_title=None, side_bar_hierarchy=None, title_style=None, side_bar_style=None):
		if side_bar_title:
			self.side_bar_title = side_bar_title
		if side_bar_hierarchy:
			self.side_bar_hierarchy = side_bar_hierarchy
		if title_style:
			self.title_style = title_style
		if side_bar_style:
			self.side_bar_style = side_bar_style

	def setNavBarInfo(self, user_name=None, user_img_path=None):
		if user_name:
			self.userName = user_name
		if user_img_path:
			self.userImg = user_img_path

	def setLoaderType(self, loader_type=None):
		if loader_type:
			self.loaderType = loader_type				# ("Bean_Eater" / "Blocks" / "Double_Ring" / "Ellipsis" / "Gear" / "Infinity" / "Pulse" / "Spinner")

	def setColorTheme(self):
		innerScript = ""

		innerScript += "document.documentElement.style.setProperty('--main-color', '" + self.main_color + "');"
		innerScript += "document.documentElement.style.setProperty('--sub-color', '" + self.sub_color + "');"
		innerScript += "document.documentElement.style.setProperty('--white-color', '" + self.dark_color + "');"
		innerScript += "document.documentElement.style.setProperty('--dark-color', '" + self.white_color + "');"
		innerScript += "document.documentElement.style.setProperty('--light-grey-color', '" + self.light_grey_color + "');"
		innerScript += "document.documentElement.style.setProperty('--semi-grey-color', '" + self.semi_grey_color + "');"
		return"""
	    <script>
	    %s
	    </script>
	    """ % (innerScript)

	def setDashboardHTMLHeader(self):
	    """
	    Return the html header for the dashboard
	    """
	    return """<meta charset="utf-8"/>
	    <meta name="viewport" content="width=device-width, initial-scale=1" />
	    <meta name="theme-color" content="#000000" />
	    <meta
	      name="description"
	      content="%s"
	    />
	    <title>%s</title>

	    <link href="%s/static/css/index.css" rel="stylesheet" media="screen">
	    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
	    <script src="%s/static/js/cookie_utils.js"></script>%s""" % (self.desc, self.title, self.main_url, self.main_url, self.uploadFileHeader())

	def uploadFileHeader(self):
	    return"""
	    <!--upload-->
	    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" crossorigin="anonymous">
	    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.min.css" crossorigin="anonymous">
	    
	    <!--event calendar-->
	    <link href='%s/static/css/fullcalendar.css' rel='stylesheet' />
	    <link href='%s/static/css/fullcalendar.print.css' rel='stylesheet' media='print' />
	    <script src='%s/static/js/jquery-1.10.2.js' type="text/javascript"></script>
	    <script src='%s/static/js/jquery-ui.custom.min.js' type="text/javascript"></script>
	    <script src='%s/static/js/fullcalendar_zh.js' type="text/javascript"></script>

	    <!--side bar-->
	    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/boxicons@2.0.8/css/boxicons.min.css"></link>

	    <!--input password-->
	    <script type="text/javascript" src="%s/static/js/password_strength_lightweight.js"></script>
	    <link rel="stylesheet" type="text/css" href="%s/static/css/password_strength.css">

	    <!--input form-->
	    <script src='%s/static/js/before_input_submit.js' type="text/javascript"></script>

	    <!--input list-->
	    <script src="%s/static/js/input_list.js"></script>

	    <!--generate loader-->
	    <script src="%s/static/js/generate_loader.js"></script>

	    <!--fblock extra function-->
	    <script src="%s/static/js/fblock_extra_func.js"></script>
	    <script src="%s/static/user_js/fblock_cus_func.js"></script>

	    """ % tuple([self.main_url for _ in range(12)])

	def setDashboardJavaScript(self):
	    return"""
	    <!--table-->
	    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
	    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
	    <script src="https://unpkg.com/bootstrap-table@1.18.3/dist/bootstrap-table.min.js"></script>
	    """

	def setDashboardSideBar(self):
	    """
	    icon library (version 2.0.8) => https://boxicons.com/
	    list with key -> path
	    side_bar_hierarchy = [
	        {"main_title1": "maintitle1/a"},
	        {"main_title2": [
	            {"sub_title21": "maintitle2/a"}, 
	            {"sub_title22": "maintitle2/b"}
	        ]}
	    ]
	    title_style = "bx-grid-alt"
	    side_bar_style = {"main_title1": "bxl-docker", "main_title2": "bxl-python"}
	    """
	    if self.withLogin:
	        login_class = ""
	    else:
	        login_class = "display_none"

		defalut_icon = "bx-grid-alt"
	    list_of_icon = list(self.side_bar_style.keys())

	    return_html = ''
	    btn_html = ''
	    for top_level in self.side_bar_hierarchy:
	        icon = defalut_icon
	        main_title = list(top_level.keys())[0]

	        if main_title in list_of_icon:
	            icon = self.side_bar_style[main_title]

	        if not isinstance(top_level[main_title], list):
	            btn_html += '<div><button type="submit" name="side_bar_btn" value="' + top_level[main_title] + '" class="nav_link toggle_class display_flex"><i class="bx ' + icon + ' nav_icon"></i><span class="nav_name">' + main_title + '</span></button></div>'

	        else:
	            sub_btn_html = ''
	            for sub_level in top_level[main_title]:
	                sub_title = list(sub_level.keys())[0]
	                sub_icon = defalut_icon
	                if sub_title in list_of_icon:
	                    sub_icon = self.side_bar_style[sub_title]
	                sub_btn_html += '<button type="submit" name="side_bar_btn" value="' + sub_level[sub_title] + '" class="nav_link toggle_class display_flex"><i class="bx ' + sub_icon + ' nav_icon"></i><span class="nav_name">' + sub_title + '</span></button>'
	            btn_html += '<div><div onclick="btnClickedFunc(this)" class="nav_link toggle_class display_flex"><i class="bx ' + icon + ' nav_icon"></i><span class="nav_name">' + main_title + '</span></div><div class="sub_title">' + sub_btn_html + '</div></div>'


	    return"""<form id="side-bar" action="/dashboard" method="post">
	    <div class="l-navbar" id="nav-bar">
	        <div class="nav">
	            <div>
	                <button type="submit" name="side_bar_btn" value="-" class="nav_logo toggle_class display_flex">
	                    <i class='bx %s nav_logo-icon'></i>
	                    <span class="nav_logo-name nav_name">%s</span>
	                </button>
	                <div class="nav_list">%s</div>
	            </div>
	            <button type="submit" name="side_bar_btn" value="logout" class="nav_link toggle_class display_flex %s">
	                <i class='bx bx-log-out nav_icon'></i>
	                <span class="nav_name">登出</span>
	            </button>
	        </div>
	    </div>
	    </form>""" % (self.title_style, self.side_bar_title, btn_html, login_class)

	def setDashboardNavBar(self):
	    if self.withLogin:
	        login_class = ""
	    else:
	        login_class = "display_none"

	    return"""<div class="nav_bar">
	        <div class="header_toggle">
	            <i class='bx bx-menu' id="header-toggle"></i>
	        </div>
	        <button class="member_section %s" onclick="window.location.href='/dashboard/profile'">
	            <img src="%s" id="user_icon">
	            <h3 id="user_name">%s</h3>
	        </button>
	    </div>
	    <script src='%s/static/js/side_bar.js' type="text/javascript"></script>""" % (login_class, self.userImg, self.userName, self.main_url)

	def setLoader(self):
	    self.loaderType = self.loaderType if self.loaderType else "Spinner"
	    return '<div id="loading_holder" style="display: none;"><div id="loader"></div></div><script>generate_loader("' + self.loaderType + '")</script>'

	def render(self):
		html_template = "login.html" if self.styleName == "login" else "index.html"

		html_header = self.setDashboardHTMLHeader()
		content, extra_script = user_defined_contents(self.path)
		content, extra_script = "", ""
		end_js = self.setDashboardJavaScript()
		color_theme = self.setColorTheme()
		load_spinner = self.setLoader()

		side_bar = None if self.styleName == "login" else self.setDashboardSideBar()
		nav_bar = None if self.styleName == "login" else self.setDashboardNavBar()

			
		return render_template(html_template, load_spinner=load_spinner, color_theme=color_theme, html_header=html_header, side_bar=side_bar, nav_bar=nav_bar, content=content, extra_script=extra_script, end_js=end_js)

if __name__ == '__main__':
	f_style = FamcyStyle("history")
	f_style.setHeadScript("title", "desc")
	f_style.setColor("#edaf00")
	f_style.setLoaderType("Double_Ring")
	f_style.setSideBarInfo(current_app.config.get("side_bar_title", ""), current_app.config.get("side_bar_hierachy", []), title_style="bxs-store", side_bar_style={"豆漿預約": "bx-coffee-togo", "豆日子商店": "bx-shopping-bag", "歷史訂單": "bx-history", "客服": "bxs-phone", "總覽": "bx-book-open"})
	f_style.setNavBarInfo("登入", os.path.join(self.main_url, "static", "image/login.png"))

	print(f_style.render())