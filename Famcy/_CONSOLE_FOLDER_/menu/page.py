import Famcy
import json
import requests
import copy
from gadgethiServerUtils.authentication import *
from gadgethiServerUtils.file_basics import read_config_yaml
from os.path import expanduser
import datetime
from _static_.store_btn_utils import *


G = GadgethiHMAC256Encryption("uber-server", Famcy.FManager.get_credentials("gadgethi_secret"))
HEADER = G.getGServerAuthHeaders()
HOST_ADDRESS = "http://127.0.0.1:5088" # "https://store.nexuni-api.com/doday/v1"
DEFAULT_MENU = '全日菜單'

class menuPage(Famcy.FamcyPage):
    def __init__(self):
        super(menuPage, self).__init__()

        self.store_id = self.get_cookie('store_id')
        self.current_main_menu = DEFAULT_MENU

        # preload function
        self.menu_data = self.get_return_menu()
        self.addon_data, self.addon_extra_info = self.get_get_addon_items()

        # for declaration
        # ===============
        self.menu_card_list = []
        self.addon_card_list = []
        self.card_0 = self.card0(self.menu_data['main_menu_info'])
        self.generate_menu_card(self.menu_data)
        self.generate_addon_card(self.addon_data)

        self.main_menu_card = self._main_menu_card()
        self.main_menu_edit_card = self._main_menu_edit_card()
        self.menu_edit_card = self._menu_edit_card()
        # ===============

        self.layout.addWidget(self.card_0, 0, 0, 1, 2)

        self.layout.addStaticWidget(self.main_menu_card)
        self.layout.addStaticWidget(self.main_menu_edit_card)
        self.layout.addStaticWidget(self.menu_edit_card)

        set_store_btn(self, '/menu')

        
    # background task function 
    # ====================================================
    # ====================================================
    # ====================================================


    # card
    # ====================================================
    def card0(self, menu_list=[]):
        _card0 = Famcy.FamcyCard()
        _card0.title = "豆日子菜單總覽"

        _input_form1 = Famcy.input_form()

        _card0.menu_list = Famcy.inputList()
        _card0.menu_list.set_submit_value_name('main_menu')
        _card0.menu_list.update({
            'title':'菜單',
            'value':[i['name'] for i in menu_list],
            'defaultValue':self.current_main_menu
        })
        _card0.menu_list.connect(self.switch_main_menu)

        _edit_sb = Famcy.submitBtn()
        _edit_sb.set_btn_style(5)
        _edit_sb.update({'title': '編輯主菜單'})
        _edit_sb.connect(self.edit_main_menu)

        _add_sb = Famcy.submitBtn()
        _add_sb.set_btn_style(5)
        _add_sb.update({'title': '新增主菜單'})
        _add_sb.connect(self.add_main_menu)

        _delete_sb = Famcy.submitBtn()
        _delete_sb.set_btn_style(5)
        _delete_sb.update({'title': '刪除主菜單'})
        _delete_sb.connect(self.delete_main_menu)

        _input_form1.layout.addWidget(_card0.menu_list, 0, 0, 1, 10)
        _input_form1.layout.addWidget(_edit_sb, 1, 0)
        _input_form1.layout.addWidget(_add_sb, 1, 1)
        _input_form1.layout.addWidget(_delete_sb, 1, 2, 1, 8)

        self.category_list = Famcy.displayParagraph()
        self.category_list.update({
                "title": "菜單類別種類",
                "content": ""
            })

        self.addon_list = Famcy.displayParagraph()
        self.addon_list.update({
                "title": "選配種類",
                "content": ""
            })

        _input_form2 = Famcy.input_form()

        add_category_btn = Famcy.submitBtn()
        add_category_btn.addon_flag = False
        add_category_btn.update({'title': '新增菜單類別'})
        add_category_btn.connect(self.add_main_item)

        add_addon_btn = Famcy.submitBtn()
        add_addon_btn.addon_flag = True
        add_addon_btn.update({'title': '新增配料類別'})
        add_addon_btn.connect(self.add_main_item)

        _input_form2.layout.addWidget(add_category_btn, 0, 0)
        _input_form2.layout.addWidget(add_addon_btn, 0, 1)

        _card0.layout.addWidget(_input_form1, 0, 0, 1, 2)
        _card0.layout.addWidget(self.category_list, 1, 0, 1, 2)
        _card0.layout.addWidget(self.addon_list, 1, 2, 1, 2)
        _card0.layout.addWidget(_input_form2, 2, 0)

        return _card0

    def menu_card(self, title, menu_data):
        _menu_card = Famcy.FamcyCard()
        _menu_card.title = title

        _input_form = Famcy.input_form()

        _menu_card.table = Famcy.table_block()
        _menu_card.table.set_submit_value_name('name')
        _menu_card.table.update({
            'category':title,
            'input_button':'radio',
            'input_value_col_field':'name',
            'page_detail':False,
            'page_detail_content':'key_value',
            'toolbar':False,
            'page_footer':False,
            'table_height':'auto',
            'column':[
                [{
                    'title': '系列',
                    'field': 'category',
                    'rowspan': 1,
                    'align': 'center',
                    'valign': 'middle',
                    'sortable': True},
                {
                    'title': '品名',
                    'field': 'name',
                    'rowspan': 1,
                    'align': 'center',
                    'valign': 'middle',
                    'sortable': True},
                {
                    'title': '配料',
                    'field': 'addon_title',
                    'rowspan': 1,
                    'align': 'center',
                    'valign': 'middle',
                    'sortable': True},
                {
                    'title': '單價',
                    'field': 'price',
                    'rowspan': 1,
                    'align': 'center',
                    'valign': 'middle',
                    'sortable': True}]
                ],
                'data':menu_data
            })

        _edit_sb = Famcy.submitBtn()
        _edit_sb.addon_flag = False
        _edit_sb.update({'title': '編輯菜單'})
        _edit_sb.connect((self.edit_item), target=(_menu_card.table))
        
        _add_sb = Famcy.submitBtn()
        _add_sb.addon_flag = False
        _add_sb.update({'title': '新增菜單'})
        _add_sb.connect((self.add_item), target=(_menu_card.table))
        
        _delete_sb = Famcy.submitBtn()
        _delete_sb.addon_flag = False
        _delete_sb.update({'title': '刪除菜單'})
        _delete_sb.connect(self.delete_item)
        
        _edit_main_sb = Famcy.submitBtn()
        _edit_main_sb.set_btn_style(5)
        _edit_main_sb.addon_flag = False
        _edit_main_sb.title = title
        _edit_main_sb.update({'title': '編輯類別名稱'})
        _edit_main_sb.connect(self.edit_main_item)
        
        _delete_main_sb = Famcy.submitBtn()
        _delete_main_sb.set_btn_style(5)
        _delete_main_sb.addon_flag = False
        _delete_main_sb.title = title
        _delete_main_sb.update({'title': '刪除菜單類別'})
        _delete_main_sb.connect(self.delete_main_item)
        
        _input_form.layout.addWidget(_edit_main_sb, 0, 0)
        _input_form.layout.addWidget(_delete_main_sb, 0, 1)
        _input_form.layout.addWidget(_menu_card.table, 1, 0, 1, 10)
        _input_form.layout.addWidget(_edit_sb, 2, 0)
        _input_form.layout.addWidget(_add_sb, 2, 1)
        _input_form.layout.addWidget(_delete_sb, 2, 2)
        
        _menu_card.layout.addWidget(_input_form, 0, 0)
        
        return _menu_card

    def addon_card(self, title, addon_data):
        _addon_card = Famcy.FamcyCard()
        _addon_card.title = title

        for i in addon_data:
            i.update({'mode': '單選' if self.addon_extra_info[title]['mode'] == 'single' else '多選'})
            
        _input_form = Famcy.input_form()

        _addon_card.table = Famcy.table_block()
        _addon_card.table.set_submit_value_name('name')
        _addon_card.table.update({
            'category':title,
            'input_button':'radio',
            'input_value_col_field':'name',
            'toolbar':False,
            'page_footer':False,
            'table_height':'auto',
            'column':[
                [{
                    'title': '系列',
                    'field': 'category',
                    'rowspan': 1,
                    'align': 'center',
                    'valign': 'middle',
                    'sortable': True},
                {
                    'title': '選項',
                    'field': 'name',
                    'rowspan': 1,
                    'align': 'center',
                    'valign': 'middle',
                    'sortable': True},
                {
                    'title': '選項加價',
                    'field': 'price',
                    'rowspan': 1,
                    'align': 'center',
                    'valign': 'middle',
                    'sortable': True},
                {
                    'title': '選配種類',
                    'field': 'mode',
                    'rowspan': 1,
                    'align': 'center',
                    'valign': 'middle',
                    'sortable': True}]
                ],
            'data':addon_data
        })

        _edit_sb = Famcy.submitBtn()
        _edit_sb.addon_flag = True
        _edit_sb.update({'title': '編輯菜單'})
        _edit_sb.connect((self.edit_item), target=(_addon_card.table))
        
        _add_sb = Famcy.submitBtn()
        _add_sb.addon_flag = True
        _add_sb.update({'title': '新增菜單'})
        _add_sb.connect((self.add_item), target=(_addon_card.table))
        
        _delete_sb = Famcy.submitBtn()
        _delete_sb.addon_flag = True
        _delete_sb.update({'title': '刪除菜單'})
        _delete_sb.connect(self.delete_item)
        
        _edit_main_sb = Famcy.submitBtn()
        _edit_main_sb.set_btn_style(5)
        _edit_main_sb.addon_flag = True
        _edit_main_sb.title = title
        _edit_main_sb.update({'title': '編輯類別名稱'})
        _edit_main_sb.connect(self.edit_main_item)
        
        _delete_main_sb = Famcy.submitBtn()
        _delete_main_sb.set_btn_style(5)
        _delete_main_sb.addon_flag = True
        _delete_main_sb.title = title
        _delete_main_sb.update({'title': '刪除菜單類別'})
        _delete_main_sb.connect(self.delete_main_item)
        
        _input_form.layout.addWidget(_edit_main_sb, 0, 0)
        _input_form.layout.addWidget(_delete_main_sb, 0, 1)
        _input_form.layout.addWidget(_addon_card.table, 1, 0, 1, 10)
        _input_form.layout.addWidget(_edit_sb, 2, 0)
        _input_form.layout.addWidget(_add_sb, 2, 1)
        _input_form.layout.addWidget(_delete_sb, 2, 2)
        
        _addon_card.layout.addWidget(_input_form, 0, 0)
        
        return _addon_card
    # ====================================================
    # ====================================================


    # prompt card
    # ====================================================
    def _main_menu_card(self):
        _main_menu_card = Famcy.FamcyCard()
        _main_menu_card.title = '新增主菜單'

        _main_menu_input_form = Famcy.input_form()

        _main_menu_card.name = Famcy.pureInput()
        _main_menu_card.name.set_submit_value_name('name')
        _main_menu_card.name.update({'input_type':'text', 'title':'主菜單名稱*'})
        
        _return_sb = Famcy.submitBtn()
        _return_sb.set_btn_style(3)
        _return_sb.update({'title': '返回'})
        _return_sb.connect(self.closed_card)
        
        _submit_sb = Famcy.submitBtn()
        _submit_sb.set_btn_style(3)
        _submit_sb.update({'title': '確定新增或更改'})
        _submit_sb.connect(self.submit_add_or_edit_level1_menu)
        
        _main_menu_input_form.layout.addWidget(_main_menu_card.name, 0, 0, 1, 2)
        _main_menu_input_form.layout.addWidget(_return_sb, 1, 0)
        _main_menu_input_form.layout.addWidget(_submit_sb, 1, 1)
        
        _main_menu_card.layout.addWidget(_main_menu_input_form, 0, 0)
        
        return _main_menu_card

    def _main_menu_edit_card(self):
        _main_menu_edit_card = Famcy.FamcyCard()
        _main_menu_edit_card.title = '新增菜單類別'

        _main_menu_edit_input_form = Famcy.input_form()

        _main_menu_edit_card.category = Famcy.pureInput()
        _main_menu_edit_card.category.set_submit_value_name('category')
        _main_menu_edit_card.category.update({'input_type':'text','title':'系列名稱*'})
        
        _main_menu_edit_card.mode = Famcy.inputList()
        _main_menu_edit_card.mode.set_submit_value_name('mode')
        _main_menu_edit_card.mode.update({
            'title':'選配模式*',
            'value':['單選', '多選'],
            'returnValue':['single', 'multiple']
        })

        _return_sb = Famcy.submitBtn()
        _return_sb.set_btn_style(3)
        _return_sb.update({'title': '返回'})
        _return_sb.connect(self.closed_card)

        _submit_sb = Famcy.submitBtn()
        _submit_sb.set_btn_style(3)
        _submit_sb.update({'title': '確定新增或更改'})
        _submit_sb.connect(self.submit_add_or_edit_main_menu)

        _main_menu_edit_input_form.layout.addWidget(_main_menu_edit_card.category, 0, 0, 1, 2)
        _main_menu_edit_input_form.layout.addWidget(_main_menu_edit_card.mode, 1, 0, 1, 2)
        _main_menu_edit_input_form.layout.addWidget(_return_sb, 2, 0)
        _main_menu_edit_input_form.layout.addWidget(_submit_sb, 2, 1)
        
        _main_menu_edit_card.layout.addWidget(_main_menu_edit_input_form, 0, 0)
        
        return _main_menu_edit_card

    def _menu_edit_card(self):
        _menu_edit_card = Famcy.FamcyCard()
        _menu_edit_card.title = '絕配系列'

        self.menu_edit_input_form = Famcy.input_form()

        _menu_edit_card.item_name = Famcy.pureInput()
        _menu_edit_card.item_name.set_submit_value_name('name')
        _menu_edit_card.item_name.update({'input_type':'text', 'title':'品名名稱'})
        
        _menu_edit_card.item_price = Famcy.pureInput()
        _menu_edit_card.item_price.set_submit_value_name('price')
        _menu_edit_card.item_price.update({'input_type':'number', 'title':'價錢'})
        
        _menu_edit_card.item_addon_choice = Famcy.multipleChoicesRadioInput()
        _menu_edit_card.item_addon_choice.set_submit_value_name('addon_choice')
        _menu_edit_card.item_addon_choice.connect(self.selected_addon_btn)
        _menu_edit_card.item_addon_choice.update({
            'title':'配料',
            'desc':'',
            'value':self.addon_titles
        })
        _menu_edit_card.item_addon = []

        _return_sb = Famcy.submitBtn()
        _return_sb.set_btn_style(3)
        _return_sb.update({'title': '返回'})
        _return_sb.connect(self.closed_card)

        _submit_sb = Famcy.submitBtn()
        _submit_sb.set_btn_style(3)
        _submit_sb.update({'title': '確定新增或更改'})
        _submit_sb.connect(self.submit_add_or_edit_menu)

        self.menu_edit_input_form.layout.addWidget(_menu_edit_card.item_name, 0, 0, 1, 2)
        self.menu_edit_input_form.layout.addWidget(_menu_edit_card.item_price, 1, 0, 1, 2)
        self.menu_edit_input_form.layout.addWidget(_menu_edit_card.item_addon_choice, 2, 0, 1, 2)
        self.menu_edit_input_form.layout.addWidget(_return_sb, 3, 0)
        self.menu_edit_input_form.layout.addWidget(_submit_sb, 3, 1)
        
        _menu_edit_card.layout.addWidget(self.menu_edit_input_form, 0, 0)
        
        return _menu_edit_card
    # ====================================================
    # ====================================================


    # submission function
    # ====================================================
    # level 1
    # =======================
    # =======================
    def switch_main_menu(self, sb, info):
        if self.update_main_menu(info['main_menu']):
            return self.update_menu('init')

    def delete_main_menu(self, sb, info):
        level = 1
        res_ind, res_msg = self.post_delete_item(self.current_main_menu, level)
        if res_ind:
            if self.update_main_menu(DEFAULT_MENU):
                return_res = self.update_menu('init')
                return return_res + [Famcy.UpdateAlert(target=(self.card_0), alert_message=' 成功刪除品項')]
            return Famcy.UpdateAlert(target=(sb.origin.parent.parent), alert_message=res_msg)

    def add_main_menu(self, sb, info):
        self.main_menu_card.current_action = 'add'
        self.clear_main_menu_card()
        return Famcy.UpdatePrompt(target=(self.main_menu_card))

    def edit_main_menu(self, sb, info):
        self.main_menu_card.title = self.current_main_menu
        self.main_menu_card.current_action = 'edit'
        self.update_main_menu_card({'name': self.current_main_menu})
        return Famcy.UpdatePrompt(target=(self.main_menu_card))

    def submit_add_or_edit_level1_menu(self, sb, info):
        if self.main_menu_card.current_action == 'add':
            extra_info = {'other_information_dict': json.dumps({'uber': {'service_availability': [{'day_of_week':'monday',  'time_periods':[{'start_time':'11:00',  'end_time':'21:00'}]}, {'day_of_week':'tuesday',  'time_periods':[{'start_time':'11:00',  'end_time':'21:00'}]}, {'day_of_week':'wednesday',  'time_periods':[{'start_time':'11:00',  'end_time':'21:00'}]}, {'day_of_week':'thursday',  'time_periods':[{'start_time':'11:00',  'end_time':'21:30'}]}, {'day_of_week':'friday',  'time_periods':[{'start_time':'11:00',  'end_time':'21:30'}]}, {'day_of_week':'saturday',  'time_periods':[{'start_time':'10:30',  'end_time':'21:30'}]}, {'day_of_week':'sunday',  'time_periods':[{'start_time':'10:30',  'end_time':'21:00'}]}]}})}
            res_ind, res_msg = self.post_add_main_item(info['name'], 1, extra_info)
        else:
            if self.main_menu_card.current_action == 'edit':
                old_name = self.current_main_menu
                update_info = {'name':info['name'],
                 'level':1}
                res_ind, res_msg = self.post_edit_item(old_name, update_info)
        if res_ind:
            if self.update_main_menu(info['name']):
                return_res = self.update_menu('init')
                return return_res + [Famcy.UpdateAlert(target=(sb.origin.parent.parent), alert_message='成功新增菜單')]
            return Famcy.UpdateAlert(target=(sb.origin.parent.parent), alert_message=res_msg)

    # level 2 or 4
    # =======================
    # =======================
    def delete_main_item(self, sb, info):
        level = 4 if sb.origin.addon_flag else 2
        res_ind, res_msg = self.post_delete_item(sb.origin.title, level)
        if res_ind:
            return_res = self.update_menu(sb.origin.addon_flag)
            return return_res + [Famcy.UpdateAlert(target=(self.card_0), alert_message='成功 刪除品項')]
        return Famcy.UpdateAlert(target=(sb.origin.parent.parent), alert_message=res_msg)

    def add_main_item(self, sb, info):
        self.main_menu_edit_card.addon_flag = sb.origin.addon_flag
        self.main_menu_edit_card.current_action = 'add'
        self.clear_main_menu_edit_card(sb.origin.addon_flag)
        return Famcy.UpdatePrompt(target=(self.main_menu_edit_card))

    def edit_main_item(self, sb, info):
        self.main_menu_edit_card.title = sb.origin.title
        self.main_menu_edit_card.addon_flag = sb.origin.addon_flag
        self.main_menu_edit_card.current_action = 'edit'
        _mode = self.addon_extra_info[sb.origin.title]['mode'] if sb.origin.title in self.addon_extra_info.keys() else ""
        self.update_main_menu_edit_card({'name':sb.origin.title,'mode':_mode}, sb.origin.addon_flag)
        return Famcy.UpdatePrompt(target=(self.main_menu_edit_card))

    def submit_add_or_edit_main_menu(self, sb, info):
        if self.main_menu_edit_card.current_action == 'add':
            addon_flag = 'addon' if self.main_menu_edit_card.addon_flag else 'category'
            if addon_flag == 'addon':
                if not info['mode']:
                    return Famcy.UpdateAlert(target=(sb.origin.parent.parent), alert_message='請選擇選配模式')
            extra_info = {'other_information_dict': json.dumps({'doday': {'mode': info['mode']}})} if self.main_menu_edit_card.addon_flag else {}
            res_ind, res_msg = self.post_add_main_item(info['category'], addon_flag, extra_info)
        else:
            if self.main_menu_edit_card.current_action == 'edit':
                old_name = self.main_menu_edit_card.title
                update_info = {'name':info['category'],
                 'level':4 if self.main_menu_edit_card.addon_flag else 2}
                extra_info = {'other_information_dict': json.dumps({'doday': {'mode': info['mode']}})} if self.main_menu_edit_card.addon_flag else {}
                update_info.update(extra_info)
                print('update_info: ', update_info)
                res_ind, res_msg = self.post_edit_item(old_name, update_info)
        if res_ind:
            return_res = self.update_menu(self.main_menu_edit_card.addon_flag)
            return return_res + [Famcy.UpdateAlert(target=(sb.origin.parent.parent), alert_message='成功更新菜單')]
        return Famcy.UpdateAlert(target=(sb.origin.parent.parent), alert_message=res_msg)

    # level 3
    # =======================
    # =======================
    def edit_item(self, sb, info):
        if info['name']:
            self.menu_edit_card.addon_flag = sb.origin.addon_flag
            self.menu_edit_card.current_action = 'edit'
            _data = self.find_data_by_name(info['name'], sb.target.value['data'])
            self.update_menu_edit_card(_data, sb.origin.addon_flag)
            return Famcy.UpdatePrompt(target=(self.menu_edit_card))
        return Famcy.UpdateAlert(target=(sb.origin.parent.parent), alert_message='未選取需更 改之品項')

    def add_item(self, sb, info):
        self.menu_edit_card.addon_flag = sb.origin.addon_flag
        self.menu_edit_card.current_action = 'add'
        self.clear_menu_edit_card(sb.target.value['category'], sb.origin.addon_flag)
        return Famcy.UpdatePrompt(target=(self.menu_edit_card))

    def delete_item(self, sb, info):
        res_ind, res_msg = self.post_delete_item(info['name'])
        if res_ind:
            return_res = self.update_menu(sb.origin.addon_flag)
            return return_res + [Famcy.UpdateAlert(target=(sb.origin.parent.parent), alert_message='成功刪除品項')]
        return Famcy.UpdateAlert(target=(sb.origin.parent.parent), alert_message=res_msg)

    def selected_addon_btn(self, sb, info):
        print('info: ', info.__dict__, info.info_dict.keys(), info['addon_choice'])
        if isinstance(info['addon_choice'], list):
            self.menu_edit_card.item_addon = info['addon_choice']
        else:
            self.menu_edit_card.item_addon = [] if self.menu_edit_card.item_addon == [info['addon_choice']] or not info['addon_choice'] else [info['addon_choice']]
        self.update_addon_section(self.menu_edit_card.item_addon)
        return Famcy.UpdateBlockHtml(target=(self.menu_edit_card.item_addon_choice))

    def submit_add_or_edit_menu(self, sb, info):
        print("self.menu_edit_card.item_addon submit: ", self.menu_edit_card.item_addon)
        if self.menu_edit_card.current_action == 'add':
            addon_connection_list = []
            for n in self.menu_edit_card.item_addon:
                connect_element = {'level':4,  'name':n,
                 'connected_name':info['name'],
                 'connected_level':3}
                addon_connection_list.append(connect_element)
            else:
                item_info = {'name':info['name'],
                 'price':info['price'],
                 'addon_connection_list':addon_connection_list}
                parent_item_type = 'addon' if self.menu_edit_card.addon_flag else 'category'
                res_ind, res_msg = self.post_add_sub_item_and_connect(parent_item_type, self.menu_edit_card.title, item_info)
                if res_ind:
                    return_res = self.update_menu(self.menu_edit_card.addon_flag)
                    return return_res + [Famcy.UpdateAlert(target=(self.menu_edit_card), alert_message='成功新增品項')]
                return Famcy.UpdateAlert(target=(self.menu_edit_card), alert_message=res_msg)

        else:
            if self.menu_edit_card.current_action == 'edit':
                addon_connection_list = []
                for n in self.menu_edit_card.item_addon:
                    connect_element = {'level':4,  'name':n,
                     'connected_name':info['name'],
                     'connected_level':3}
                    addon_connection_list.append(connect_element)
                else:
                    update_info = {'name':info['name'],
                     'price':info['price'],
                     'addon_connection_list':json.dumps(addon_connection_list),
                     'level':3}
                    res_ind, res_msg = self.post_edit_item(self.menu_edit_card.item_name.value['defaultValue'], update_info)
                    if res_ind:
                        return_res = self.update_menu(self.menu_edit_card.addon_flag)
                        return return_res + [Famcy.UpdateAlert(target=(self.menu_edit_card), alert_message='成功更改品項')]
                    return Famcy.UpdateAlert(target=(self.menu_edit_card), alert_message=res_msg)

        return Famcy.UpdateAlert(target=(self.menu_edit_card), alert_message='系統異常，請重 新再試')

    def closed_card(self, sb, info):
        return Famcy.UpdateRemoveElement(prompt_flag=True)
    # ====================================================
    # ====================================================
        

    # http request function
    # ====================================================
    def get_return_menu(self):
        print('test: ', self.store_id, self.current_main_menu)
        query = HOST_ADDRESS + '?service=menu&operation=return_menu&device=doday_console&store_id=' + str(self.store_id) + '&menu_name=' + self.current_main_menu
        r = requests.get(query, headers=HEADER).text
        res_dict = json.loads(r)
        return res_dict

    def get_get_addon_items(self):
        query = HOST_ADDRESS + '?service=menu&operation=get_addon_items&store_id=' + self.store_id + '&level=4'
        r = requests.get(query, headers=HEADER).text
        res_dict = json.loads(r)
        return res_dict['message'], res_dict['extra_info']

    def post_add_main_item(self, item_name, item_type, extra_info={}):
        send_dict = {
            'service':'menu',
            'operation':'add_main_item',
            'store_id':self.store_id,
            'item_type':item_type,
            'name':item_name,
            'price':0,
            'main_menu':self.current_main_menu
        }
        send_dict.update(extra_info)
        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        res_dict = json.loads(r)
        return res_dict['indicator'], res_dict['message']

    def post_add_sub_item_and_connect(self, parent_item_type, parent_item_name, item_info):
        send_dict = {
            'service':'menu',
            'operation':'add_sub_item_and_connect',
            'store_id':self.store_id,
            'parent_item_type':parent_item_type,
            'parent_item_name':parent_item_name,
            'name':json.dumps([item_info['name']]),
            'price':json.dumps([item_info['price']]),
            'suspend':json.dumps([0]),
            'other_information_dict':json.dumps([{}]),
            'delivery_price':json.dumps([item_info['price']]),
            'addon_connection_list':json.dumps([item_info['addon_connection_list']])
        }
        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        res_dict = json.loads(r)
        return res_dict['indicator'], res_dict['message']

    def post_edit_item(self, old_name, update_info):
        send_dict = {
            'service':'menu',
            'operation':'edit_item',
            'store_id':self.store_id,
            'old_name':old_name
        }
        send_dict.update(update_info)
        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        res_dict = json.loads(r)
        return res_dict['indicator'], res_dict['message']

    def post_delete_item(self, name, level=3):
        send_dict = {
            'service':'menu',
            'operation':'delete_item',
            'store_id':self.store_id,
            'name':name,
            'level':level
        }
        r = requests.post(HOST_ADDRESS, data=send_dict, headers=HEADER).text
        res_dict = json.loads(r)
        return res_dict['indicator'], res_dict['message']
    # ====================================================
    # ====================================================


    # utils
    # ====================================================
    def clear_main_menu_card(self):
        self.main_menu_card.title = '新增主菜單'
        self.main_menu_card.name.update({'defaultValue': ''})

    def update_main_menu_card(self, item_data):
        self.main_menu_card.title = item_data['name']
        self.main_menu_card.name.update({'defaultValue': item_data['name']})

    def clear_main_menu_edit_card(self, addon_flag=False):
        self.main_menu_edit_card.title = '新增配料類別' if addon_flag else '新增菜單類別'
        self.main_menu_edit_card.category.update({'defaultValue': ''})
        if addon_flag:
            self.main_menu_edit_card.mode.show()
        else:
            self.main_menu_edit_card.mode.hide()

    def update_main_menu_edit_card(self, item_data, addon_flag=False):
        self.main_menu_edit_card.title = item_data['name']
        self.main_menu_edit_card.category.update({'defaultValue': item_data['name']})
        if addon_flag:
            self.main_menu_edit_card.mode.show()
            _mode = '單選' if item_data['mode'] == 'single' else '多選'
            self.main_menu_edit_card.mode.update({'defaultValue': _mode})
        else:
            self.main_menu_edit_card.mode.hide()

    def clear_menu_edit_card(self, _title, addon_flag=False):
        self.menu_edit_card.title = _title
        self.menu_edit_card.item_name.update({'defaultValue': ''})
        self.menu_edit_card.item_price.update({'defaultValue': ''})
        self.menu_edit_card.item_addon = []
        self.update_addon_section('X', addon_flag)

    def update_menu_edit_card(self, item_data, addon_flag=False):
        self.menu_edit_card.title = item_data['category']
        self.menu_edit_card.item_name.update({'defaultValue': item_data['name']})
        self.menu_edit_card.item_price.update({'defaultValue': item_data['price'][4:] if isinstance(item_data['price'], str) else str(item_data['price'])})
        self.menu_edit_card.item_addon = [] if addon_flag else copy.deepcopy(item_data['addon_title'])
        self.update_addon_section(self.menu_edit_card.item_addon, addon_flag)

    def update_addon_section(self, addon_data, addon_flag=False):
        if addon_flag:
            self.menu_edit_card.item_addon_choice.hide()
        else:
            self.menu_edit_card.item_addon_choice.show()
            if isinstance(addon_data, list) and len(addon_data) > 1:
                _addon_d = '|'.join(list(addon_data))
            elif isinstance(addon_data, list) and len(addon_data) == 1:
                _addon_d = addon_data[0]
            elif isinstance(addon_data, str):
                _addon_d = addon_data
            else:
                _addon_d = "X"
            self.menu_edit_card.item_addon_choice.update({'title':'配料','desc':str('選配種類: ')+str(_addon_d),'defaultValue':addon_data})
            
    def update_title_list(self, title_block, title_list):
        title_block.update({'content': '<br>'.join(title_list)})

    def generate_menu_card(self, menu_data):
        self.titles = menu_data['titles']
        self.items = menu_data['items']
        self.avail = menu_data['avail']
        self.menu_card_list = self.remove_cards_from_page(self.menu_card_list)
        x = 1
        for t, i, a in zip(menu_data['titles'], menu_data['items'], menu_data['avail']):
            m = self.menu_card(t, i)
            self.menu_card_list.append(m)
            self.layout.addWidget(m, x, 0)
            x += 1
        else:
            self.update_title_list(self.category_list, menu_data['titles'])

    def generate_addon_card(self, addon_data):
        self.addon_titles = list(addon_data.keys())
        self.addon_card_list = self.remove_cards_from_page(self.addon_card_list)
        x = 1
        for t in self.addon_titles:
            m = self.addon_card(t, addon_data[t])
            self.addon_card_list.append(m)
            self.layout.addWidget(m, x, 1)
            x += 1
        else:
            self.update_title_list(self.addon_list, self.addon_titles)

    def remove_cards_from_page(self, card_list):
        for c in card_list:
            self.layout.removeWidget(c)
        else:
            return []

    def find_data_by_name(self, name, data):
        for d in data:
            if name == d['name']:
                return d

    def update_menu(self, addon_flag):
        self.menu_data = self.get_return_menu()
        self.addon_data, self.addon_extra_info = self.get_get_addon_items()
        if addon_flag == 'init':
            self.card_0.menu_list.update({'value':[i['name'] for i in self.menu_data['main_menu_info']],  'defaultValue':self.current_main_menu})
            self.generate_menu_card(self.menu_data)
            self.generate_addon_card(self.addon_data)
            self.menu_edit_card.item_addon_choice.update({'value': self.addon_titles})
        else:
            if addon_flag:
                self.generate_addon_card(self.addon_data)
                self.menu_edit_card.item_addon_choice.update({'value': self.addon_titles})
            else:
                self.card_0.menu_list.update({'defaultValue': self.current_main_menu})
                self.generate_menu_card(self.menu_data)
        return [Famcy.UpdateTabHtml(target=self)]

    def update_main_menu(self, name):
        if self.current_main_menu != name:
            self.current_main_menu = name
            self.set_cookie('main_menu', self.current_main_menu)
            return True
        return False
    # ====================================================
    # ====================================================

   
menuPage.register("/menu", Famcy.NexuniStyle(), permission_level=0, background_thread=False)