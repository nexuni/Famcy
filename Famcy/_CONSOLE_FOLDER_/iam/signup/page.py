import Famcy

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

def signup_submission(submission_list, **configs):

    name = sub_list[0][0]
    email = sub_list[1][0]
    password = sub_list[2][0]

    user = FamcyUser.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        submission_dict_handler = Famcy.SijaxSubmit("update_alert")
        submission_dict_handler.alert_setting.update({"alert_type":"alert-danger"})
        return submission_dict_handler.return_submit_info("註冊失敗")
    else:
        profile_pic_url = current_app.config.get("default_profile_pic_url", "")

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = FamcyUser(email=email, name=name, profile_pic_url=profile_pic_url,\
          password=generate_password_hash(password, method='sha256'))

        submission_dict_handler = Famcy.SijaxSubmit("redirect_page")
        return submission_dict_handler.return_submit_info("main.home")

PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT, [signup_submission])


