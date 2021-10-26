import Famcy

class ProfilePage(Famcy.FamcyPage):
    def __init__(self):
        super(ProfilePage, self).__init__("/iam/profile", style)

CHANGE_PROFILE_INFO_BTN_NAME = "送出修改"
CHANGE_PROFILE_PIC_BTN_NAME = "更新大頭貼"

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

def edit_member_info_submission(submission_list, **configs):
    name = sub_list[0][0]
    email = sub_list[1][0]
    password = sub_list[2][0]

    user = FamcyUser.query.filter_by(email=current_user.email).first()

    if name != "":
        user.name = name
    if email != "":
        user.email = email
    if password != "":
        user.password = password

    Famcy.db.session.commit()

    obj_response.script("$('#loading_holder').css('display','none');")
    inner_text, extra_script = generate_alert({"alert_type":"alert-warning", "alert_message":"資訊修改成功", "alert_position":"prepend"}, form_id)        
    obj_response.html_prepend('#'+block_id, inner_text)
    obj_response.script(extra_script)
    obj_response.redirect(url_for('iam.profile_page'))

# def edit_profile_pic_submission(submission_list, **configs):
#     pass





# if sub_list[0][0] != "":
#   img_data = base64.b64decode(sub_list[0][0])
#   index = int(sub_list[0][2])
#   with open("./static/image/FamcyUserProfilePic." + sub_list[0][1].split(".")[1], "wb") as fh:
#       fh.write(img_data)

#   user = FamcyUser.query.filter_by(email=current_user.email).first()
#   user.profile_pic_url = "../static/image/FamcyUserProfilePic." + sub_list[0][1].split(".")[1]
#   Famcy.db.session.commit()
    
#   obj_response.script("$('#loading_holder').css('display','none');")
#   inner_text, extra_script = generate_alert({"alert_type":"alert-warning", "alert_message":"照片修改成功", "alert_position":"prepend"}, form_id)        
#   obj_response.html_prepend('#'+block_id, inner_text)
#   obj_response.script(extra_script)
#   obj_response.redirect(url_for('iam.profile_page'))

# else:
#   obj_response.script("$('#loading_holder').css('display','none');")
#   inner_text, extra_script = generate_alert({"alert_type":"alert-warning", "alert_message":"未上傳照片", "alert_position":"prepend"}, form_id)     
#   obj_response.html_prepend('#'+block_id, inner_text)
#   obj_response.script(extra_script)

PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT, [None, None, None])