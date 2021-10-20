import Famcy
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user

# Define Famcy User
class FamcyUser(UserMixin):

	def setup_user_loader(self):
		"""
		This is the function to setup flask login user
		login manager user loader function. 
		"""
		def load_user(user_id):
			# since the user_id is just the primary key of our user table, use it in the query for the user
			# return FamcyUser.query.get(int(user_id))

			print("user_id: ", user_id)

			# Famcy.LOGIN_BEFORE()

			get_str = Famcy.FManager.http_client.client_get(Famcy.LOGIN_URL, Famcy.LOGIN_API, gauth=True)
			get_ind = json.loads(get_str)["indicator"]
			get_msg = json.loads(get_str)["message"]

			print("get_ind: ", get_ind)

			if get_ind:
				# Famcy.LOGIN_AFTER(get_str)
				print("Famcy.user: ", Famcy.FManager["FamcyUser"])
				return Famcy.FManager["FamcyUser"]
			return None

		Famcy.FManager["LoginManager"].user_loader(load_user)