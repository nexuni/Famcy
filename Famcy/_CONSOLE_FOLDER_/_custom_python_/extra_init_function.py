from gadgethiServerUtils.GadgethiClient import *
from gadgethiServerUtils.file_basics import *
import Famcy
import json

CONFIG_FILE_PATH = Famcy.USER_DEFAULT_FOLDER + "_custom_python_/member_config.yaml"

def member_load_config():
    data = read_config_yaml(CONFIG_FILE_PATH)
    return data

yaml_config = member_load_config()
CLIENT_SERVER = GadgetHiClient(**yaml_config)
global_var = {"title": "CLIENT_SERVER", "action": CLIENT_SERVER}



# login section
# ======================================================================================================
login_url = {"title": "LOGIN_URL", "action": "member_http_url"}				# cannot change title name

login_dict = {
	"service": "member",
	"operation": "get_member_info"
}
login_api = {"title": "LOGIN_API", "action": login_dict}					# cannot change title name

def login_before_action():
	pass

def login_after_action(res_str):
	print("login_after_action res_str: ", res_str)
	res_msg = json.loads(json.loads(res_str)["message"])
	print("login_after_action res_msg: ", res_msg, type(res_msg))
	Famcy.user.phone_num = str(res_msg["user_phone"])
	Famcy.user.name = res_msg["username"] if res_msg["username"] != "" else Famcy._current_app.config.get("default_name", "")
	Famcy.user.profile_pic_url = res_msg["profile_pic_url"] if res_msg["profile_pic_url"] != "" else Famcy._current_app.config.get("default_profile_pic_url", "")

login_before = {"title": "LOGIN_BEFORE", "action": login_before_action}		# cannot change title name
login_after = {"title": "LOGIN_AFTER", "action": login_after_action}		# cannot change title name
# ======================================================================================================


EXTRA_ACTION = []
EXTRA_GLOBAL_VAR = [global_var]

LOGIN_VAR = [login_url, login_api, login_before, login_after]