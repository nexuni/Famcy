import enum
import Famcy

class FamcyPermissionLevel(enum.IntEnum):
	Guest = 0
	Member = 1
	Admin = 2

class FamcyPermissions:
	"""
	This represents the permission 
	structure of FamcyPage
	
	Rep:
		* lowest permission level: 
		the lowest permission for the 
		page. 
	Method:
		* verify: verify the permission 
	"""
	def __init__(self, lowest_permission):
		self.lowest_permission = lowest_permission

	def verify(self, current_user):
		"""
		This is the method to verify whether
		current Famcy user met the req of 
		the permission. 
		"""
		pass