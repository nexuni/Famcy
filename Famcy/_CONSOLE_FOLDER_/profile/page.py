"""
This is the page definition file for Famcy. 
There are two variables very important, which
defines the page content: PAGE_HEADER and PAGE_CONTENT. 

PAGE_HEADER:
	* title: a list of titles of the sections on the page. It is usually put
		at the top of the section as a header. 
	* size: a list. defines section size. Options include half_inner_section
		and inner_section -> half means share two sections on one page
	* type: list of fblock type of the sections on the page. This should match the
		defined fblock name. 

PAGE_CONTENT:
	* a list of dictionary that defines the fblock sections on the page.  

example:
	PAGE_HEADER = {
	"title": ["Nexuni 員工後台"],
	"size": ["inner_section"],
	"type": ["display"]
}

PAGE_CONTENT = [
	{
		"values": [{
			"type": "displayParagraph",
			"title": "",
			"content": '''
**Nexuni 会社ウェブサイトの案内** 

	1. 希望能讓來到Nexuni的新朋友都能夠快速地學習並瞭解我們工作時會使用到的軟體、程式語言、工具等等。
	2. 作為能力考核的依據
	3. 整合所有公司內部的管理工具，如發票上傳、PO申請、報帳工具、打卡記錄等

快速入門:

	* 點擊總覽 -> 訓練網介紹（可以看到本網頁的所有的內容簡介
	* 點擊相關訓練內容 -> 開始練習
	* 點擊總覽 -> 學習進度裡面的進度報告（可以看到練習的成果）

（網頁內容的版權皆為Nexuni Co. 擁有）
''',
		},{
			"type": "displayTag",
			"title": "測試不知道這是用來幹嘛的Layout",
			"content": "到底Display Tag有什麼不一樣？",
		},
		{
			"type": "displayImage",
			"title": "下面這個解析度也太糟糕了吧",
			"img_name": "test.jpg", # This is gathered from static folder or _images_ user folder
		}]
	}
]
"""
import Famcy
import json
# from flask import url_for


PAGE_HEADER = {
    "title": ["Famcy 會員資訊頁面", "修改會員資料", "上傳新個人頭像"],
    "size": ["onethird_inner_section", "onethird_inner_section", "onethird_inner_section"],
    "type": ["display", "input_form", "upload_form"]
}

display_image_block = Famcy.display.generate_values_content("displayImage")
display_image_block.update({
        "title": "個人頭像",
        "img_name": [Famcy._current_user.profile_pic_url],
        "img_size": ["100%"]
    })

display_name = Famcy.display.generate_values_content("displayTag")
display_name.update({
        "title": "姓名: ",
        "content": Famcy._current_user.name,
    })

display_phone_num = Famcy.display.generate_values_content("displayTag")
display_phone_num.update({
        "title": "電話號碼: ",
        "content": Famcy._current_user.phone_num,
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
        "placeholder": Famcy._current_user.name,
        "mandatory": False
    })

input_form_content = Famcy.input_form.generate_template_content([name_content, password_content])
input_form_content.update({
        "loader": True,
        "main_button_name": ["送出修改"], # btn name in same section must not be same
        "action_after_post": "clean",                    # (clean / save)
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
    "main_button_name": ["更新大頭貼"], # btn name in same section must not be same
})

display_content = Famcy.display.generate_template_content([display_image_block, display_name, display_phone_num])

def edit_info(submission_list, **configs):
    temp = {}
    update_name = submission_list[0][0]
    update_password = submission_list[1][0]

    msg = ""

    if update_password != "":
        temp["password"] = update_password

        msg += "密碼、"

    if update_name != "":
        temp["username"] = update_name

        msg += "姓名、"

    if msg != "":

        send_dict = {
            "service": "member",
            "operation": "edit_member_info", 
            "user_phone": Famcy._current_user.phone_num,
            "edit_info_dict": temp
        }

        post_str = Famcy.FManager.http_client.client_post("member_http_url", send_dict, gauth=True)
        post_ind = json.loads(post_str)["indicator"]
        post_msg = json.loads(post_str)["message"]

        if post_ind:
            msg = msg[:-2] + "已成功修改"

            if update_name != "":
                Famcy._current_user.name = update_name

                PAGE_CONTENT_OBJECT[0].context["values"][1].update({
                    "content": update_name
                })
                PAGE_CONTENT_OBJECT[1].context["values"][0].update({
                    "placeholder": update_name
                })

        else:
            msg = msg[:-2] + "修改失敗，請重新再試"

    submission_dict_handler = Famcy.SijaxSubmit("update_alert")
    update_tab_handler = Famcy.SijaxSubmit("redirect_page_tab")


    temp_list = []
    temp_list.extend(submission_dict_handler.return_submit_info(msg=msg))
    temp_list.extend(update_tab_handler.return_submit_info(msg="profile"))
    return temp_list


def edit_pic(submission_list, **configs):
    update_pic = submission_list[0][0]

    if update_pic != "":

        send_dict = {
            "service": "member",
            "operation": "edit_member_info", 
            "user_phone": Famcy._current_user.phone_num,
            "edit_info_dict": {},
            "picture_data": update_pic
        }

        post_str = Famcy.FManager.http_client.client_post("member_http_url", send_dict, gauth=True)
        post_ind = json.loads(post_str)["indicator"]
        post_msg = json.loads(post_str)["message"]

        print("post_msg: ", post_msg)

        if post_ind:
            msg = "照片已成功修改，仍需時間上傳，請稍後確認"

            Famcy._current_user.profile_pic_url = update_pic

        else:
            msg = "照片修改失敗，請重新再試"

    submission_dict_handler = Famcy.SijaxSubmit("update_alert")
    return submission_dict_handler.return_submit_info(msg=msg)

PAGE_CONTENT = [display_content, input_form_content, upload_form_content]
PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT, [None, edit_info, edit_pic])