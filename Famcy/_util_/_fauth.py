import abc
import Famcy
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user

class FLogin(metaclass=abc.ABCMeta):
	"""
	Represent the login manager
	that helps authenticate famcy
	users to famcy applications. 
	"""
	def __init__(self, always_remember=True):
		self.always_remember = always_remember

	def login_famcy_user(self, user):
		login_user(user, remember=self.always_remember)

	def logout_famcy_user(self):
		logout_user()

	def register(self):
		Famcy.FamcyLoginManager = self

	@abc.abstractmethod
	def load_famcy_user(self, user_id):
		"""
		This is the function to load
		famcy user object with user_id
		"""
		pass

	@abc.abstractmethod
	def prelogin(self, user):
		pass

	@abc.abstractmethod
	def postlogin(self, user):
		pass

# Define Famcy User
class FamcyUser(UserMixin):

	def __init__(self):
		self.login_manager = Famcy.FamcyLoginManager

	@classmethod
	def setup_user_loader(cls):
		"""
		This is the function to setup flask login user
		login manager user loader function. 
		"""
		def load_user(user_id):

			self.login_manager.load_famcy_user(user_id)
			# since the user_id is just the primary key of our user table, use it in the query for the user
			# return FamcyUser.query.get(int(user_id))

			print("user_id: ", user_id)

			# Famcy.LOGIN_BEFORE()

			# get_str = Famcy.FManager.http_client.client_get(Famcy.LOGIN_URL, Famcy.LOGIN_API, gauth=True)
			# get_ind = json.loads(get_str)["indicator"]
			# get_msg = json.loads(get_str)["message"]

			# print("get_ind: ", get_ind)

			# if get_ind:
			# 	# Famcy.LOGIN_AFTER(get_str)
			# 	print("Famcy.user: ", Famcy.FManager["FamcyUser"])
			return cls()
			# return None

		Famcy.FManager["LoginManager"].user_loader(load_user)