import Famcy
import json
import requests
import copy
from gadgethiServerUtils.authentication import *
from gadgethiServerUtils.file_basics import read_config_yaml
from os.path import expanduser
import datetime


G = GadgethiHMAC256Encryption("uber-server", Famcy.FManager.get_credentials("gadgethi_secret"))
HEADER = G.getGServerAuthHeaders()
STORE_ID = "DDC"
HOST_ADDRESS = "http://127.0.0.1:5088" # "https://store.nexuni-api.com/doday/v1"

class menuPage(Famcy.FamcyPage):
    def __init__(self):
        super(menuPage, self).__init__()

        # preload function
        self.menu_data = self.get_return_menu()
        self.addon_data = self.get_get_addon_items()

        # for declaration
        # ===============
        self.menu_card_list = []
        self.addon_card_list = []
        self.card_0 = self.card0()
        self.menu_card_list = self.generate_menu_card(self.menu_data)
        self.addon_card_list = self.generate_addon_card(self.addon_data)

        self.menu_edit_card = self._menu_edit_card()
        # ===============

        self.layout.addWidget(self.card_0, 0, 0, 1, 2)

        self.layout.addStaticWidget(self.menu_edit_card)

        
    # background task function 
    # ====================================================
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card0(self):
        _card0 = Famcy.FamcyCard()
        _card0.title = "豆日子菜單總覽"

        self.category_list = Famcy.displayParagraph()
        self.category_list.update({
                "title": "菜單類別種類",
                "content": """
(1) 絕配系列<br>
(2) 豆花自選<br>
(3) 紫米自選<br>
(4) 綠豆湯自選<br>
(5) 純享系列<br>
                """
            })

        self.addon_list = Famcy.displayParagraph()
        self.addon_list.update({
                "title": "選配種類",
                "content": """
(1) 冰量<br>
(2) 甜度<br>
                """
            })

        _input_form = Famcy.input_form()

        add_category_btn = Famcy.submitBtn()
        add_category_btn.update({
                "title": "新增菜單類別"
            })

        add_addon_btn = Famcy.submitBtn()
        add_addon_btn.update({
                "title": "新增配料類別"
            })
        add_addon_btn.connect(self.add_menu)

        _input_form.layout.addWidget(add_category_btn, 0, 0)
        _input_form.layout.addWidget(add_addon_btn, 0, 1)

        _card0.layout.addWidget(self.category_list, 0, 0, 1, 2)
        _card0.layout.addWidget(self.addon_list, 0, 2, 1, 2)
        _card0.layout.addWidget(_input_form, 1, 0)

        return _card0

    def menu_card(self, title, menu_data):
        _menu_card = Famcy.FamcyCard()
        _menu_card.title = title

        _input_form = Famcy.input_form()

        _table = Famcy.table_block()
        _table.set_submit_value_name("name")
        _table.update({
            "category": title,
            "input_button": "radio",
            "input_value_col_field": "name", 

            "page_detail": False,                            # (true / false)
            "page_detail_content": "key_value",             # if page_detail == true: (key_value / HTML_STR => ["<p>line1</p>", "<p>line2</p>"])

            "toolbar": False,                                # (true / false)
            "page_footer": False,

            "table_height": "auto",

            "column": [[{
                    "title": '系列',
                    "field": 'category',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '品名',
                    "field": 'name',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '配料',
                    "field": 'addon_title',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '單價',
                    "field": 'price',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                }
            ]],
            "data": menu_data
        })

        _edit_sb = Famcy.submitBtn()
        _edit_sb.addon_flag = False
        _edit_sb.update({
                "title": "編輯菜單"
            })
        _edit_sb.connect(self.edit_menu, target=_table)

        _add_sb = Famcy.submitBtn()
        _add_sb.addon_flag = False
        _add_sb.update({
                "title": "新增菜單"
            })
        _add_sb.connect(self.add_menu, target=_table)

        _delete_sb = Famcy.submitBtn()
        _delete_sb.update({
                "title": "刪除菜單"
            })
        _delete_sb.connect(self.delete_menu)

        _input_form.layout.addWidget(_table, 0, 0, 1, 10)
        _input_form.layout.addWidget(_edit_sb, 1, 0)
        _input_form.layout.addWidget(_add_sb, 1, 1)
        _input_form.layout.addWidget(_delete_sb, 1, 2)

        _menu_card.layout.addWidget(_input_form, 0, 0)

        return _menu_card

    def addon_card(self, title, addon_data):
        _addon_card = Famcy.FamcyCard()
        _addon_card.title = title

        _input_form = Famcy.input_form()

        _table = Famcy.table_block()
        _table.set_submit_value_name("name")
        _table.update({
            "category": title,
            "input_button": "radio",
            "input_value_col_field": "name", 

            "toolbar": False,                                # (true / false)
            "page_footer": False,

            "table_height": "auto",

            "column": [[{
                    "title": '系列',
                    "field": 'category',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },{
                    "title": '選項',
                    "field": 'name',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": '選項加價',
                    "field": 'price',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                }
            ]],
            "data": addon_data
        })

        _edit_sb = Famcy.submitBtn()
        _edit_sb.addon_flag = True
        _edit_sb.update({
                "title": "編輯菜單"
            })
        _edit_sb.connect(self.edit_menu, target=_table)

        _add_sb = Famcy.submitBtn()
        _add_sb.addon_flag = True
        _add_sb.update({
                "title": "新增菜單"
            })
        _add_sb.connect(self.add_menu, target=_table)

        _delete_sb = Famcy.submitBtn()
        _delete_sb.update({
                "title": "刪除菜單"
            })
        _delete_sb.connect(self.delete_menu)

        _input_form.layout.addWidget(_table, 0, 0, 1, 10)
        _input_form.layout.addWidget(_edit_sb, 1, 0)
        _input_form.layout.addWidget(_add_sb, 1, 1)
        _input_form.layout.addWidget(_delete_sb, 1, 2)

        _addon_card.layout.addWidget(_input_form, 0, 0)

        return _addon_card
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    def _menu_edit_card(self):
        _menu_edit_card = Famcy.FamcyCard()
        _menu_edit_card.title = "絕配系列"

        self.menu_edit_input_form = Famcy.input_form()

        _menu_edit_card.category = Famcy.pureInput()
        _menu_edit_card.category.set_submit_value_name("category")
        _menu_edit_card.category.update({
                "input_type": "text",
                "title": "系列名稱"
            })

        _menu_edit_card.item_name = Famcy.pureInput()
        _menu_edit_card.item_name.set_submit_value_name("name")
        _menu_edit_card.item_name.update({
                "input_type": "text",
                "title": "品名名稱"
            })

        _menu_edit_card.item_price = Famcy.pureInput()
        _menu_edit_card.item_price.set_submit_value_name("price")
        _menu_edit_card.item_price.update({
                "input_type": "number",
                "title": "價錢"
            })

        # _menu_edit_card.item_addon_title = Famcy.displayParagraph()
        # _menu_edit_card.item_addon_title.update({
        #         "title": "配料",
        #         "content": ""
        #     })

        # self.menu_edit_section = Famcy.FamcySection()

        # btn_col, i = 4, 0
        # for addon in self.addon_titles:
        #     _ = Famcy.submitBtn()
        #     _.selected = False
        #     _.update({ "title": addon })
        #     _.connect(self.selected_addon_btn)
        #     self.menu_edit_section.layout.addWidget(_, int(i/btn_col), i%btn_col, 1, 1, "addon"+str(i))
        #     i += 1

        _menu_edit_card.item_addon_choice = Famcy.multipleChoicesRadioInput()
        _menu_edit_card.item_addon_choice.set_submit_value_name("addon_choice")
        _menu_edit_card.item_addon_choice.connect(self.selected_addon_btn)
        _menu_edit_card.item_addon_choice.update({
                "title": "配料",
                "desc": "",
                "value": self.addon_titles,
            })

        _menu_edit_card.item_addon = []

        _return_sb = Famcy.submitBtn()
        _return_sb.set_btn_style(3)
        _return_sb.update({ "title": "返回" })
        _return_sb.connect(self.closed_card)

        _submit_sb = Famcy.submitBtn()
        _submit_sb.set_btn_style(3)
        _submit_sb.update({ "title": "確定新增或更改" })
        _submit_sb.connect(self.submit_add_or_edit_menu)

        self.menu_edit_input_form.layout.addWidget(_menu_edit_card.category, 0, 0, 1, 2)
        self.menu_edit_input_form.layout.addWidget(_menu_edit_card.item_name, 1, 0, 1, 2)
        self.menu_edit_input_form.layout.addWidget(_menu_edit_card.item_price, 2, 0, 1, 2)
        self.menu_edit_input_form.layout.addWidget(_menu_edit_card.item_addon_choice, 3, 0, 1, 2)
        self.menu_edit_input_form.layout.addWidget(_return_sb, 4, 0)
        self.menu_edit_input_form.layout.addWidget(_submit_sb, 4, 1)

        _menu_edit_card.layout.addWidget(self.menu_edit_input_form, 0, 0)

        return _menu_edit_card
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    def edit_menu(self, sb, info):
        if info["name"]:
            self.menu_edit_card.addon_flag = sb.origin.addon_flag
            self.menu_edit_card.current_action = "edit"
            _data = self.find_data_by_name(info["name"], sb.target.value["data"])
            self.update_menu_edit_card(_data, sb.origin.addon_flag)                       # , addon_flag=True
            return Famcy.UpdatePrompt(target=self.menu_edit_card)
        else:
            return Famcy.UpdateAlert(target=sb.origin.parent.parent, alert_message="未選取需更改之品項")

    def add_menu(self, sb, info):
        self.menu_edit_card.addon_flag = sb.origin.addon_flag
        self.menu_edit_card.current_action = "add"
        self.clear_menu_edit_card(sb.target.value["category"], sb.origin.addon_flag)      # , addon_flag=True
        return Famcy.UpdatePrompt(target=self.menu_edit_card)

    def delete_menu(self, sb, info):
        res_ind, res_msg = self.post_delete_item(info["name"])
        if res_ind:
            return Famcy.UpdateAlert(target=sb.origin.parent.parent, alert_message="成功刪除品項")
        else:
            return Famcy.UpdateAlert(target=sb.origin.parent.parent, alert_message=res_msg)

    def selected_addon_btn(self, sb, info):
        print("info: ", info.__dict__, info.info_dict["addon_choice"])
        self.menu_edit_card.item_addon = info.info_dict["addon_choice"]
        self.update_addon_section(self.menu_edit_card.item_addon)

        # if sb.origin.selected:
        #     if sb.origin.value["title"] in self.menu_edit_card.item_addon:
        #         self.menu_edit_card.item_addon.remove(sb.origin.value["title"])
        #     self.update_addon_section(self.menu_edit_card.item_addon)
        # else:
        #     if sb.origin.value["title"] not in self.menu_edit_card.item_addon:
        #         self.menu_edit_card.item_addon.append(sb.origin.value["title"])
        #     self.update_addon_section(self.menu_edit_card.item_addon)

        return Famcy.UpdateBlockHtml(target=self.menu_edit_card.item_addon_choice)

        

    def submit_add_or_edit_menu(self, sb, info):
        if self.menu_edit_card.current_action == "add":
            addon_connection_list = []
            for n in self.menu_edit_card.item_addon:
                connect_element = {
                    "level": 4,
                    "name": n,
                    "connected_name": info["name"],
                    "connected_level": 3,
                }
                addon_connection_list.append(connect_element)

            item_info = {
                "name": info["name"],
                "price": info["price"],
                "addon_connection_list": addon_connection_list
            }
            res_ind, res_msg = self.post_add_sub_item_and_connect(2, info["category"], item_info)
            if res_ind:
                return Famcy.UpdateAlert(target=self.menu_edit_card, alert_message="成功新增品項")
            else:
                return Famcy.UpdateAlert(target=self.menu_edit_card, alert_message=res_msg)

        elif self.menu_edit_card.current_action == "edit":
            addon_connection_list = []
            for n in self.menu_edit_card.item_addon:
                connect_element = {
                    "level": 4,
                    "name": n,
                    "connected_name": info["name"],
                    "connected_level": 3,
                }
                addon_connection_list.append(connect_element)

            print("addon_connection_list: ", addon_connection_list)
            update_info = {
                "name": info["name"],
                "price": info["price"],
                "addon_connection_list": json.dumps(addon_connection_list)
            }
            res_ind, res_msg = self.post_edit_item(self.menu_edit_card.item_name.value["defaultValue"], update_info)
            if res_ind:
                return Famcy.UpdateAlert(target=self.menu_edit_card, alert_message="成功更改品項")
            else:
                return Famcy.UpdateAlert(target=self.menu_edit_card, alert_message=res_msg)

        return Famcy.UpdateAlert(target=self.menu_edit_card, alert_message="系統異常，請重新再試")

    def closed_card(self, sb, info):
        return Famcy.UpdateRemoveElement(prompt_flag=True)
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    def get_return_menu(self):
        query = HOST_ADDRESS+"?service=menu&operation=return_menu&device=doday_console&store_id="+str(STORE_ID)
        r = requests.get(query, headers=HEADER).text
        res_dict = json.loads(r)
        # print("res_dict: ", res_dict)
        return res_dict

    def get_get_addon_items(self):
        query = HOST_ADDRESS+"?service=menu&operation=get_addon_items&store_id="+STORE_ID+"&level=4"
        r = requests.get(query, headers=HEADER).text
        res_dict = json.loads(r)
        # print("res_dict: ", res_dict["message"])
        return res_dict["message"]

    def post_add_sub_item_and_connect(self, parent_item_type, parent_item_name, item_info):
        send_dict = {
            "service": "menu",
            "operation": "add_sub_item_and_connect",
            "store_id": STORE_ID,
            "parent_item_type": parent_item_type,
            "parent_item_name": parent_item_name,
            "name": json.dumps([item_info["name"]]),
            "price": json.dumps([item_info["price"]]),
            "suspend": json.dumps([0]),
            "other_information_dict": json.dumps([{}]),
            "delivery_price": json.dumps([item_info["price"]]),
            "addon_connection_list": json.dumps([item_info["addon_connection_list"]]),
        }
        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        res_dict = json.loads(r)
        print("res_dict: ", res_dict["message"])
        return res_dict["indicator"], res_dict["message"]

    def post_edit_item(self, old_name, update_info):
        send_dict = {
            "service": "menu",
            "operation": "edit_item",
            "store_id": STORE_ID,
            "old_name": old_name,
            "level": 3
        }
        send_dict.update(update_info)
        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        res_dict = json.loads(r)
        print("post_edit_item: ", res_dict["message"])
        return res_dict["indicator"], res_dict["message"]

    def post_delete_item(self, name):
        send_dict = {
            "service": "menu",
            "operation": "delete_item",
            "store_id": STORE_ID,
            "name": name,
            "level": 3
        }
        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        res_dict = json.loads(r)
        # print("res_dict: ", res_dict["message"])
        return res_dict["indicator"], res_dict["message"]
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    def clear_menu_edit_card(self, _title, addon_flag=False):
        self.menu_edit_card.title = _title
        self.menu_edit_card.category.update({ "defaultValue": "" })
        self.menu_edit_card.item_name.update({ "defaultValue": "" })
        self.menu_edit_card.item_price.update({ "defaultValue": "" })
        self.menu_edit_card.item_addon = []
        self.update_addon_section("X", addon_flag)

    def update_menu_edit_card(self, item_data, addon_flag=False):
        self.menu_edit_card.title = item_data["category"]
        self.menu_edit_card.category.update({ "defaultValue": item_data["category"] })
        self.menu_edit_card.item_name.update({ "defaultValue": item_data["name"] })
        self.menu_edit_card.item_price.update({ "defaultValue": item_data["price"][4:] if isinstance(item_data["price"], str) else str(item_data["price"])})
        self.menu_edit_card.item_addon = None if addon_flag else copy.deepcopy(item_data["addon_title"])
        self.update_addon_section(self.menu_edit_card.item_addon, addon_flag)

    def update_addon_section(self, addon_data, addon_flag=False):
        if addon_flag:
            self.menu_edit_card.item_addon_choice.hide()
            # self.menu_edit_card.item_addon_choice.update({ "title": "", "desc": "" })
            # self.display_addon_section(addon_data, addon_flag)
        else:
            self.menu_edit_card.item_addon_choice.show()
            self.menu_edit_card.item_addon_choice.update({ "title": "配料", "desc": "選配種類: "+("|".join(addon_data)), "defaultValue": addon_data })
            # self.display_addon_section(addon_data)
    
    # def display_addon_section(self, addon_data):
    #     for i in self.menu_edit_section.item_addon_choice.value["value"]:
    #         if i in self.menu_edit_card.item_addon:
    #             t.selected = True
    #             t.set_btn_style(4)
    #         else:
    #             t.selected = False
    #             t.set_btn_style(2)

    def update_title_list(self, title_block, title_list):
        title_block.update({ "content": "<br>".join(title_list) })

    def generate_menu_card(self, menu_data):
        self.titles = menu_data["titles"]
        self.items = menu_data["items"]
        self.avail = menu_data["avail"]
        self.remove_cards_from_page(self.menu_card_list)
        x = 1
        for t, i, a in zip(menu_data["titles"], menu_data["items"], menu_data["avail"]):
            m = self.menu_card(t, i)
            self.menu_card_list.append(m)
            self.layout.addWidget(m, x, 0)
            x += 1
        self.update_title_list(self.category_list, menu_data["titles"])

    def generate_addon_card(self, addon_data):
        self.addon_titles = list(addon_data.keys())
        self.remove_cards_from_page(self.addon_card_list)
        x = 1
        for t in self.addon_titles:
            m = self.addon_card(t, addon_data[t])
            self.addon_card_list.append(m)
            self.layout.addWidget(m, x, 1)
            x += 1
        self.update_title_list(self.addon_list, self.addon_titles)

    def remove_cards_from_page(self, card_list):
        for c in card_list:
            self.layout.removeWidget(c)
        card_list = []

    def find_data_by_name(self, name, data):
        for d in data:
            if name == d["name"]:
                return d
        return None
    # ====================================================
    # ====================================================

   
menuPage.register("/menu", Famcy.NexuniStyle(), permission_level=0, background_thread=False)