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
	def login(self, user):
		pass

# Define Famcy User
class FUser(UserMixin):
	def __init__(self):
		self.id = str(id(self))
		self.level = 0

	@classmethod
	def setup_user_loader(cls):
		"""
		This is the function to setup flask login user
		login manager user loader function. 
		"""
		def load_user(user_id):
			return Famcy.FamcyLoginManager.load_famcy_user(user_id)

		Famcy.FManager["LoginManager"].user_loader(load_user)

