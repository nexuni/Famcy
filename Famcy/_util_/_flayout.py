import enum
import Famcy
import random

class FamcyLayoutMode(enum.IntEnum):
	default = 0
	recommend = 1
	custom = 2

class FamcyCustomLayoutType:
	def __init__(self):
		self.defaultContent = None			# [[card, start row, start col, height(num row), width(num col)] ...]
		self.type = []						# [None / "device"]
		self.max = []						# [None / "500px" ...]
		self.min = []						# [None / "500px" ...]
		self.orientation = []				# [None / "portrait" / "landscape"]
		self.layoutContent = []				# [[[card, start row, start col, height(num row), width(num col)] ...]]

	def generateCssMode(self, index):
		mode = "@media only screen "
		if self.type[index]:
			self.type[index] += "-"
		else:
			self.type[index] = ""
		if self.max[index]:
			mode += "(max-" + self.type[index] + "width: " + self.max[index] + ") and "
		if self.min[index]:
			mode += "(min-" + self.type[index] + "width: " + self.min[index] + ") and "
		if self.orientation[index]:
			mode += "(orientation: " + self.orientation[index] + ") and"

		return mode[:-4]

	def generateFamcyLayoutDict(self):
		return_dict = {}
		if self.defaultContent:
			return_dict["default"] = self.defaultContent
		for i in range(len(self.layoutContent)):
			if self.layoutContent[i]:
				return_dict[self.generateCssMode(i)] = self.layoutContent[i]
		return return_dict

	def setCustomLayoutContent(self, _type=None, _max=None, _min=None, _orientation=None, _layoutContent=None):
		self.type.append(_type)
		self.max.append(_max)
		self.min.append(_min)
		self.orientation.append(_orientation)
		self.layoutContent.append(_layoutContent)

	def setDefaultContent(self, defaultContent):
		self.defaultContent = defaultContent

class FamcyRecommendLayoutType:
	def __init__(self):
		self.defaultContent = None
		self.browsers960LayoutContent = None
		self.browsers1440LayoutContent = None
		self.browsers2000LayoutContent = None
		self.phoneLayoutContent = None
		self.ipadLayoutContent = None
		self.ipadLayoutContentV = None
		self.ipadLayoutContentH = None

	def generateFamcyLayoutDict(self):
		return_dict = {}
		if self.defaultContent:
			return_dict["default"] = self.defaultContent
		if self.browsers960LayoutContent:
			return_dict["@media only screen and (min-width: 960px)"] = self.browsers960LayoutContent
		if self.browsers1440LayoutContent:
			return_dict["@media only screen and (min-width: 1440px)"] = self.browsers1440LayoutContent
		if self.browsers2000LayoutContent:
			return_dict["@media only screen and (min-width: 2000px)"] = self.browsers2000LayoutContent
		if self.phoneLayoutContent:
			return_dict["@media only screen and (max-device-width: 480px)"] = self.phoneLayoutContent
		if self.ipadLayoutContent:
			return_dict["@media only screen and (device-width: 768px)"] = self.ipadLayoutContent
		if self.ipadLayoutContentV:
			return_dict["@media only screen and (min-device-width: 481px) and (max-device-width: 1024px) and (orientation:portrait)"] = self.ipadLayoutContentV
		if self.ipadLayoutContentH:
			return_dict["@media only screen and (min-device-width: 481px) and (max-device-width: 1024px) and (orientation:landscape)"] = self.ipadLayoutContentH
		
		return return_dict

	def setDefaultContent(self, defaultContent):
		self.defaultContent = defaultContent

	def setBrowserLayoutContent(self, content960=None, content1440=None, content2000=None):
		if content960:
			self.browsers960LayoutContent = content960
		if content1440:
			self.browsers1440LayoutContent = content1440
		if content2000:
			self.browsers2000LayoutContent = content2000

	def setPhoneLayoutContent(self, contentPhone=None):
		if contentPhone:
			self.phoneLayoutContent = contentPhone

	def setipadLayoutContent(self, contentipad=None, contentipadV=None, contentipadH=None):
		if contentipad:
			self.ipadLayoutContent = contentipad
		if contentipadV:
			self.ipadLayoutContentV = contentipadV
		if contentipadH:
			self.ipadLayoutContentH = contentipadH



class FamcyLayoutType:
	def __init__(self, layout_mode=FamcyLayoutMode.default):
		self.mode = layout_mode					# (FamcyLayoutMode.reommend, FamcyLayoutMode.custom, FamcyLayoutMode.default)
		self.layoutClass = FamcyRecommendLayoutType() if self.mode == FamcyLayoutMode.reommend else FamcyCustomLayoutType()

	def getLayoutDict(self):
		return self.layoutClass.generateFamcyLayoutDict()



class FamcyLayout:
	"""
	This represents the layout scheme
	that the famcy console would need
	to obtain. 

	AF(layout_mode): Represent a layout with mode
	layout_mode

	Rep:
		* content: a list of list of [card, start row, 
			start col, height(num row), width(num col)]

	Method:
		* setMode(layout mode)
		* addWidget(card, start row, start col, height(num row), width(num col))
		* render()
	"""
	def __init__(self, layout_mode):
		self.mode = layout_mode
		self.layoutType = FamcyLayoutType(self.mode)

		self.content = []
		self._check_rep()

	def _check_rep(self):
		"""
		Rep Invariant
		"""
		pass

	def setMode(self, layout_mode):
		"""
		This is the method to set the
		layout mode of the famcy layout. 
		"""
		self.mode = layout_mode

	def addWidget(self, card, start_row, start_col, height=1, width=1):
		self.content.append([card, int(start_row), int(start_col), int(height), int(width)])

	def clearContent(self):
		self.content = []

	def updateDefaultContent(self):
		self.layoutType.layoutClass.setDefaultContent(self.content)
		self.clearContent()

	def updateCustomLayoutContent(self, _type=None, _max=None, _min=None, orientation=None):
		if self.mode == FamcyLayoutMode.custom:
			self.layoutType.layoutClass.setCustomLayoutContent(_type, _max, _min, orientation, self.content)
			self.clearContent()

	def updateBrowserLayoutContent960(self):
		if self.mode == FamcyLayoutMode.reommend:
			self.layoutType.layoutClass.setBrowserLayoutContent(content960=self.content)
			self.clearContent()

	def updateBrowserLayoutContent1440(self):
		if self.mode == FamcyLayoutMode.reommend:
			self.layoutType.layoutClass.setBrowserLayoutContent(content1440=self.content)
			self.clearContent()

	def updateBrowserLayoutContent2000(self):
		if self.mode == FamcyLayoutMode.reommend:
			self.layoutType.layoutClass.setBrowserLayoutContent(content2000=self.content)
			self.clearContent()

	def updatePhoneLayoutContent(self):
		if self.mode == FamcyLayoutMode.reommend:
			self.layoutType.layoutClass.setPhoneLayoutContent(contentPhone=self.content)
			self.clearContent()

	def updateipadLayoutContent(self):
		if self.mode == FamcyLayoutMode.reommend:
			self.layoutType.layoutClass.setipadLayoutContent(contentipad=self.content)
			self.clearContent()

	def updateipadLayoutContent(self):
		if self.mode == FamcyLayoutMode.reommend:
			self.layoutType.layoutClass.setipadLayoutContent(contentipadV=self.content)
			self.clearContent()

	def updateipadLayoutContent(self):
		if self.mode == FamcyLayoutMode.reommend:
			self.layoutType.layoutClass.setipadLayoutContent(contentipadH=self.content)
			self.clearContent()

	def setLayout(self):
		layoutDict = self.layoutType.getLayoutDict()
		cssLayout = '<style type="text/css">'

		for i, (k, v) in enumerate(layoutDict.items()):
			if k == "default":
				cssLayout += self.setDeviceLayout(v)
			else:
				cssLayout += k + " {"
				cssLayout += self.setDeviceLayout(v)
				cssLayout += "}"

		cssLayout += '</style>'

		return cssLayout

	def setDeviceLayout(self, content):
		cssLayout = ""
		for card in content:
			cssLayout += """
			#%s {
				grid-row-start: %s;
				grid-column-start: %s;
				grid-column-end: %s;
	  			grid-row-end: %s;
			}
			""" % (card[0].id, str(card[1] + 1), str(card[2] + 1), str(card[2] + card[4] + 1), str(card[1] + card[3] + 1))

		return cssLayout

	def render(self):
		layout_css = self.setLayout()
		render_html = ""
		return layout_css + render_html

# Tests
# -----------
class _card:
	def __init__(self):
		self.id = "id_" + str(random.randint(0,1000))
		

if __name__ == '__main__':
	layout = FamcyLayout(FamcyLayoutMode.default)
	layout.addWidget(_card(), 0, 0, 2, 1)
	layout.addWidget(_card(), 0, 1)
	layout.addWidget(_card(), 1, 1)
	layout.addWidget(_card(), 2, 0, 1, 2)
	layout.updateDefaultContent()

	layout.addWidget(_card(), 0, 0, 2, 1)
	layout.addWidget(_card(), 0, 1)
	layout.addWidget(_card(), 1, 1)
	layout.addWidget(_card(), 2, 0, 1, 2)
	layout.updatePhoneLayoutContent()


	print(layout.render())
# ========================================================



