from .dashboard_utils import *
from flask_login import UserMixin, current_user

LOGIN_BTN_NAME = "登入"
CHANGE_PROFILE_INFO_BTN_NAME = "送出修改"
CHANGE_PROFILE_PIC_BTN_NAME = "更新大頭貼"
PCONTENTOBJ = []

def login_page_contents():
    """
    This is the helper function to generate
    all the contents for the login page. 
    """
    PAGE_HEADER = {
        "title": ["Famcy 登入"],
        "size": ["login_section"],
        "type": ["input_form"]
    }

    email_content = Famcy.input_form.generate_values_content("pureInput")
    email_content.update({
            "type": "pureInput",
            "title": "帳號(email)",
            "desc": "",
            "input_type": "text",                               # text / number
            "placeholder": "gadmin@nexuni.com",
            "mandatory": True
        })
    password_content = Famcy.input_form.generate_values_content("inputPassword")
    password_content.update({
            "type": "inputPassword",
            "title": "密碼",
            "desc": "",
            "mandatory": True
        })
    save_info_content = Famcy.input_form.generate_values_content("singleChoiceRadioInput")
    save_info_content.update({
            "type": "singleChoiceRadioInput",
            "title": "是否記住帳號密碼？",
            "desc": "",
            "mandatory": True,
            "value": ["是", "否"]
        })

    url_btn_content = Famcy.input_form.generate_values_content("urlBtn")
    url_btn_content.update({
            "title": "是否記住帳號密碼？",
            "desc": "",
            "url": "/signup",
            "button_name": "加入會員",
            "style": "link_style",
            "desc": "還沒有會員?"

        })

    input_form_content = Famcy.input_form.generate_template_content([email_content, password_content, save_info_content, url_btn_content])
    input_form_content.update({
            "submit_type": "submit_login_section",
            "main_button_name": [LOGIN_BTN_NAME], # btn name in same section must not be same
            "action_after_post": "save",                    # (clean / save)
            "main_desc": "",
            "loader": True
        })

    PAGE_CONTENT = [input_form_content]

    content_object = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT)

    Famcy.update_object_id(content_object, "login", "login")

    html_header = dashboardHTMLHeader(current_app.config.get("console_title", ""), current_app.config.get("console_description", ""))
    content, extra_script = generate_section_content(PAGE_HEADER, content_object, "login")
    end_js = dashboardJavaScript()
    color_theme = setColorTheme(main_color="#edaf00")
    load_spinner = generateLoader("Double_Ring")

    return html_header, content, extra_script, end_js, content_object, color_theme, load_spinner

def signin_page_contents():
    """
    This is the helper function to generate
    all the contents for the signin page. 
    """
    
    PAGE_HEADER = {
        "title": ["Famcy 會員註冊"],
        "size": ["login_section"],
        "type": ["input_form"]
    }

    email_content = Famcy.input_form.generate_values_content("pureInput")
    email_content.update({
            "type": "pureInput",
            "title": "帳號(email)",
            "desc": "",
            "input_type": "text",                               # text / number
            "placeholder": "gadmin@nexuni.com",
            "mandatory": True
        })
    password_content = Famcy.input_form.generate_values_content("inputPassword")
    password_content.update({
            "type": "inputPassword",
            "desc": "",
            "title": "密碼",
            "mandatory": True
        })
    name_content = Famcy.input_form.generate_values_content("pureInput")
    name_content.update({
            "type": "pureInput",
            "title": "名字",
            "desc": "",
            "input_type": "text",                               # text / number
            "placeholder": "Nexuni Admin",
            "mandatory": True
        })

    input_form_content = Famcy.input_form.generate_template_content([name_content, email_content, password_content])
    input_form_content.update({
            "submit_type": "submit_signup_section",
            "main_button_name": ["註冊"], # btn name in same section must not be same
            "action_after_post": "save",                    # (clean / save)
            "main_desc": "",
            "loader": True
        })

    PAGE_CONTENT = [input_form_content]

    content_object = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT)

    Famcy.update_object_id(content_object, "signup", "signup")

    html_header = dashboardHTMLHeader(current_app.config.get("console_title", ""), current_app.config.get("console_description", ""))
    content, extra_script = generate_section_content(PAGE_HEADER, content_object, "signup")
    end_js = dashboardJavaScript()
    color_theme = setColorTheme(main_color="#edaf00")
    load_spinner = generateLoader("Double_Ring")

    return html_header, content, extra_script, end_js, content_object, color_theme, load_spinner


def profile_page_contents():
    """
    This is the helper function to generate
    all the contents for the signin page. 
    """
    PAGE_HEADER = {
        "title": ["Famcy 會員資訊頁面", "修改會員資料", "上傳新個人頭像"],
        "size": ["onethird_inner_section", "onethird_inner_section", "onethird_inner_section"],
        "type": ["display", "input_form", "upload_form"]
    }

    display_image_block = Famcy.display.generate_values_content("displayImage")
    display_image_block.update({
            "title": "個人頭像",
            "img_name": [current_user.profile_pic_url],
            "img_size": ["100%"]
        })

    display_tag_block = Famcy.display.generate_values_content("displayTag")
    display_tag_block.update({
            "title": "姓名: ",
            "content": current_user.name,
        })

    display_tag_block2 = Famcy.display.generate_values_content("displayTag")
    display_tag_block2.update({
            "title": "Email: ",
            "content": current_user.email,
        })

    email_content = Famcy.input_form.generate_values_content("pureInput")
    email_content.update({
            "title": "Email",
            "desc": "",
            "input_type": "text",                               # text / number
            "placeholder": current_user.email,
            "mandatory": False
        })
    password_content = Famcy.input_form.generate_values_content("inputPassword")
    password_content.update({
            "title": "密碼",
            "desc": "",
            "mandatory": False
        })
    name_content = Famcy.input_form.generate_values_content("pureInput")
    name_content.update({
            "title": "姓名",
            "desc": "",
            "input_type": "text",                               # text / number
            "placeholder": current_user.name,
            "mandatory": False
        })

    input_form_content = Famcy.input_form.generate_template_content([name_content, email_content, password_content])
    input_form_content.update({
            "loader": True,
            "submit_type": "submit_profile_section",
            "main_button_name": [CHANGE_PROFILE_INFO_BTN_NAME], # btn name in same section must not be same
            "action_after_post": "save",                    # (clean / save)
        })

    upload_form_detail = Famcy.upload_form.generate_values_content("uploadFile")
    upload_form_detail.update({
            "title": "個人頭貼",
            "file_num": "single",                     # ("single", "multiple")
            "accept_type": ["png", "jpg", "heic"],
        })

    upload_form_content = Famcy.upload_form.generate_template_content([upload_form_detail])
    upload_form_content.update({
        "loader": True,
        "submit_type": "submit_profile_section",
        "main_button_name": [CHANGE_PROFILE_PIC_BTN_NAME], # btn name in same section must not be same
    })

    PAGE_CONTENT = [Famcy.display.generate_template_content([display_image_block, display_tag_block, display_tag_block2]), input_form_content, upload_form_content]

    content_object = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT)

    Famcy.update_object_id(content_object, "profile", "profile")

    content, extra_script = generate_section_content(PAGE_HEADER, content_object, "profile")
    html_header = dashboardHTMLHeader(current_app.config.get("console_title", ""), current_app.config.get("console_description", ""))
    side_bar = dashboardSideBar(current_app.config.get("side_bar_title", ""), current_app.config.get("side_bar_hierachy", {}))
    nav_bar = dashboardNavBar(current_user.name, current_user.profile_pic_url)
    end_js = dashboardJavaScript()
    color_theme = setColorTheme(main_color="#edaf00")
    load_spinner = generateLoader("Double_Ring")

    return html_header, side_bar, nav_bar, content, extra_script, end_js, content_object, color_theme, load_spinner


