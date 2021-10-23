import Famcy
import urllib
import importlib
from flask import current_app

# dashboard content utils
# --------------

# def setColorTheme(main_color="#3968F7", sub_color="#94D4ED", dark_color="#2d2d2d", white_color="#ffffff", light_grey_color="#f1f1f1", semi_grey_color="#cccccc"):
#     return"""
#     <script>
#     document.documentElement.style.setProperty('--main-color', '%s');
#     document.documentElement.style.setProperty('--sub-color', '%s');
#     document.documentElement.style.setProperty('--white-color', '%s');
#     document.documentElement.style.setProperty('--dark-color', '%s');
#     document.documentElement.style.setProperty('--light-grey-color', '%s');
#     document.documentElement.style.setProperty('--semi-grey-color', '%s');
#     </script>
#     """ % (main_color, sub_color, white_color, dark_color, light_grey_color, semi_grey_color)

# def uploadFileHeader():
#     return"""
#     <!--upload-->
#     <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" crossorigin="anonymous">
#     <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.min.css" crossorigin="anonymous">
    
#     <!--event calendar-->
#     <link href='%s/static/css/fullcalendar.css' rel='stylesheet' />
#     <link href='%s/static/css/fullcalendar.print.css' rel='stylesheet' media='print' />
#     <script src='%s/static/js/jquery-1.10.2.js' type="text/javascript"></script>
#     <script src='%s/static/js/jquery-ui.custom.min.js' type="text/javascript"></script>
#     <script src='%s/static/js/fullcalendar_zh.js' type="text/javascript"></script>

#     <!--side bar-->
#     <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/boxicons@2.0.8/css/boxicons.min.css"></link>

#     <!--input password-->
#     <script type="text/javascript" src="%s/static/js/password_strength_lightweight.js"></script>
#     <link rel="stylesheet" type="text/css" href="%s/static/css/password_strength.css">

#     <!--input form-->
#     <script src='%s/static/js/before_input_submit.js' type="text/javascript"></script>

#     <!--input list-->
#     <script src="%s/static/js/input_list.js"></script>

#     <!--generate loader-->
#     <script src="%s/static/js/generate_loader.js"></script>

#     <!--fblock extra function-->
#     <script src="%s/static/js/fblock_extra_func.js"></script>
#     <script src="%s/static/user_js/fblock_cus_func.js"></script>

#     """ % tuple([current_app.config.get("main_url", "") for _ in range(12)])

# def dashboardJavaScript():
#     return"""
#     <!--table-->
#     <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"></script>
#     <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
#     <script src="https://unpkg.com/bootstrap-table@1.18.3/dist/bootstrap-table.min.js"></script>
#     """

# def dashboardHTMLHeader(title, desc, icon_path=""):
#     """
#     Return the html header for the dashboard
#     """
#     return """<meta charset="utf-8"/>
#     <meta name="viewport" content="width=device-width, initial-scale=1" />
#     <meta name="theme-color" content="#000000" />
#     <meta
#       name="description"
#       content="%s"
#     />
#     <title>%s</title>

#     <link href="%s/static/css/index.css" rel="stylesheet" media="screen">
#     <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
#     <script src="%s/static/js/cookie_utils.js"></script>%s""" % (desc, title, current_app.config.get("main_url", ""), current_app.config.get("main_url", ""), uploadFileHeader())

# def dashboardSideBar(side_bar_title, side_bar_hierarchy, title_style="bx-game", side_bar_style={}, with_login=True):
#     """
#     icon library (version 2.0.8) => https://boxicons.com/
#     list with key -> path
#     side_bar_hierarchy = [
#         {"main_title1": "maintitle1/a"},
#         {"main_title2": [
#             {"sub_title21": "maintitle2/a"}, 
#             {"sub_title22": "maintitle2/b"}
#         ]}
#     ]
#     title_style = "bx-grid-alt"
#     side_bar_style = {"main_title1": "bxl-docker", "main_title2": "bxl-python"}
#     """
#     if with_login:
#         login_class = ""
#     else:
#         login_class = "display_none"

#     defalut_icon = "bx-grid-alt"
#     list_of_icon = list(side_bar_style.keys())

#     return_html = ''
#     btn_html = ''
#     for top_level in side_bar_hierarchy:
#         icon = defalut_icon
#         main_title = list(top_level.keys())[0]

#         if main_title in list_of_icon:
#             icon = side_bar_style[main_title]

#         if not isinstance(top_level[main_title], list):
#             btn_html += '<div><button type="submit" name="side_bar_btn" value="' + top_level[main_title] + '" class="nav_link toggle_class display_flex"><i class="bx ' + icon + ' nav_icon"></i><span class="nav_name">' + main_title + '</span></button></div>'

#         else:
#             sub_btn_html = ''
#             for sub_level in top_level[main_title]:
#                 sub_title = list(sub_level.keys())[0]
#                 sub_icon = defalut_icon
#                 if sub_title in list_of_icon:
#                     sub_icon = side_bar_style[sub_title]
#                 sub_btn_html += '<button type="submit" name="side_bar_btn" value="' + sub_level[sub_title] + '" class="nav_link toggle_class display_flex"><i class="bx ' + sub_icon + ' nav_icon"></i><span class="nav_name">' + sub_title + '</span></button>'
#             btn_html += '<div><div onclick="btnClickedFunc(this)" class="nav_link toggle_class display_flex"><i class="bx ' + icon + ' nav_icon"></i><span class="nav_name">' + main_title + '</span></div><div class="sub_title">' + sub_btn_html + '</div></div>'


#     return"""<form id="side-bar" action="/dashboard" method="post">
#     <div class="l-navbar" id="nav-bar">
#         <div class="nav">
#             <div>
#                 <button type="submit" name="side_bar_btn" value="-" class="nav_logo toggle_class display_flex">
#                     <i class='bx %s nav_logo-icon'></i>
#                     <span class="nav_logo-name nav_name">%s</span>
#                 </button>
#                 <div class="nav_list">%s</div>
#             </div>
#             <button type="submit" name="side_bar_btn" value="logout" class="nav_link toggle_class display_flex %s">
#                 <i class='bx bx-log-out nav_icon'></i>
#                 <span class="nav_name">登出</span>
#             </button>
#         </div>
#     </div>
#     </form>""" % (title_style, side_bar_title, btn_html, login_class)

# def dashboardNavBar(user_name, user_img_path, with_login=True):
#     if with_login:
#         login_class = ""
#     else:
#         login_class = "display_none"

#     return"""<div class="nav_bar">
#         <div class="header_toggle">
#             <i class='bx bx-menu' id="header-toggle"></i>
#         </div>
#         <button class="member_section %s" onclick="window.location.href='/dashboard/profile'">
#             <img src="%s" id="user_icon">
#             <h3 id="user_name">%s</h3>
#         </button>
#     </div>
#     <script src='%s/static/js/side_bar.js' type="text/javascript"></script>""" % (login_class, user_img_path, user_name, current_app.config.get("main_url", ""))


# def generateLoader(loader_type):
#     """
#     loader_type = ["Bean_Eater", "Blocks", "Double_Ring", "Ellipsis", "Gear", "Infinity", "Pulse", "Spinner"]
#     """
#     return '<div id="loading_holder" style="display: none;"><div id="loader"></div></div><script>generate_loader("' + loader_type + '")</script>'

def user_defined_contents(path, path_prefix="dashboard/"):
    """
    Helper function to add user defined
    content to the section page. 
    - Input:
        path: path to the user defined
        content. This is raw urlencoded path
    """
    header_dict, content_object = get_header_and_content(path)

    # Guard list length and header/content format
    assert isinstance(content_object, list), "PAGE_CONTENT must be a list"
    assert "type" in header_dict and "size" in header_dict and "title" in header_dict, "PAGE_HEADER must include type, size, title keys"
    assert len(content_object) == len(header_dict["type"]) and len(content_object) == len(header_dict["size"]) \
        and len(content_object) == len(header_dict["title"]), "PAGE_HEADER and PAGE_CONTENT must have same length"

    # all user_defined contents are under dashboard
    return generate_section_content(header_dict, content_object, path=path_prefix+path)

def get_header_and_content(path):
    """
    Helper function to get the header
    and content dict.  
    - Input:
        path: path to the user defined
        content. 
    """
    # Get the folder path module
    page_define_path = current_app.config.get('user_default_folder','') + path + "." + \
            current_app.config.get('user_default_page_define_file','')
    folder_module = page_define_path.replace("-", ".")
    folder_module = folder_module.replace("/", ".")
    page_module = importlib.import_module(current_app.config.get('package_name','') + "."+folder_module)
    # Start getting defined contents from folder
    header_dict = getattr(page_module, current_app.config.get("user_defined_content_header_var"))
    content_object_list = getattr(page_module, current_app.config.get("user_defined_content_object_var"))
    Famcy.update_object_id(content_object_list, current_app.config.get('package_name','') + "."+folder_module, 
            path)

    return header_dict, content_object_list

def generate_section_content(header_dict, content_object, path=""):
    """
    This is the helper function to generate
    section content html from header and content objects. 
    """
    # Start generate html content for the pages
    section_content_html = []
    section_content_extra_script = []
    for sec_size, sec_title, content_obj in zip(header_dict["size"], header_dict["title"], content_object):
        temp_dict = {}
        if type(content_obj) == list:
            temp_dict["target_id"] = str(content_obj[0].context["target_id"])
            temp_dict["tab"] = path
            content_temp = ""
            temp_dict["block_id"] = []
            for content_sub_obj in content_obj:
                temp_dict["block_id"].append(str(content_sub_obj.context["id"]))

                # generateContent must run after setting temp_dict's target_id!!!!!!!!!!
                sub_content_temp = generateContent(content_sub_obj, path)
                content_temp += sub_content_temp
                

                section_content_extra_script.append(generateLoadScript(content_sub_obj))
        else:
            temp_dict["target_id"] = str(content_obj.context["target_id"])
            temp_dict["block_id"] = [str(content_obj.context["id"])]
            temp_dict["tab"] = path

            # generateContent must run after setting temp_dict's target_id!!!!!!!!!!
            content_temp = generateContent(content_obj, path)
            section_content_extra_script.append(generateLoadScript(content_obj))

        temp_dict["size"] = sec_size
        temp_dict["title"] = sec_title
        temp_dict["content"] = content_temp
        section_content_html.append(temp_dict)

    return section_content_html, section_content_extra_script

def generateContent(content_obj, path):
    """
    This is the helper function to generate content
    for famcy. 
    - Input
        * content_obj: section object generated
        in page. 
        * path: file path of the folder
    - Return:
        return the html content from each famcy blocks
        return html fblock object
    """
    content_obj.link_submission_actions(path)
    return content_obj.render(**current_app.config)

def generateLoadScript(content_obj):
    return content_obj.load_script(**current_app.config)

def get_submission_info_dict(form_id, tab_name, block_id, response_dict):
    tab = tab_name.split("/")[-1]
    input_sec_id = form_id
    header_dict, content_list = get_header_and_content(tab)

    info_dict = {}

    for sec_type, sec_content in zip(header_dict["type"], content_list):
        # Only call the submission function if the id is matched. 
        if type(sec_content) == list:
            for sub_sec_type, sub_sec_content in zip(sec_type, sec_content):
                if input_sec_id == sub_sec_content.context["id"]:
                    info_dict = sub_sec_content.handle_submission(response_dict)

        else:
            if input_sec_id == sec_content.context["id"]:
                info_dict = sec_content.handle_submission(response_dict)

    return info_dict

def get_list_selected_action(form_id, tab_name, block_id, response_dict):
    tab = tab_name.split("/")[-1]
    input_sec_id = form_id
    header_dict, content_list = get_header_and_content(tab)

    info_dict = {}

    for sec_type, sec_content in zip(header_dict["type"], content_list):
        # Only call the submission function if the id is matched. 
        if type(sec_content) == list:
            for sub_sec_type, sub_sec_content in zip(sec_type, sec_content):
                if input_sec_id == sub_sec_content.context["id"]:
                    info_dict = sub_sec_content.handle_list_selected_action(response_dict)

        else:
            if input_sec_id == sec_content.context["id"]:
                info_dict = sec_content.handle_list_selected_action(response_dict)

    return info_dict

