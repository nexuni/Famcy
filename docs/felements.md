# Famcy Elements
This goes through how to develop your customized famcy elements and the natively provided famcy element templates.<br>
FElement is designed for Famcy development. User can edit all html attributes of the corresponding tag after initializing the FElement.<br>
<br>
### Attributes

| Attributes | Default Value | Definition |
| ---------- | ------------- | ---------- |
| children | [] (type: list, [type: FElement]) | A list that save all children elements |
| script | [] (type: list, [type: FElement]) | A list that save all static script elements |
| parentElement | None | Represent the parent element if it exists |
| html | "" (type: str) | Represent the innerHTML of the element after rendering |
| innerHTML | "" (type: str) | Represent the innerHTML of the element before rendering |
| classList | [] (type: list, [type: str]) | A list that save all class name of the corresponding html tag |
| style | {} (type: dict, {key: "type: str"}) | A dictionary that save all style attributes of the corresponding html tag |
| attributes | {} (type: dict, {key: "type: str"}) | A dictionary that save all attributes of the corresponding html tag |

<br>
### Functions

| Functions | Input Value *(default)* | Output Value | Definition |
| --------- | --------------------- | ------------ | ---------- |
| addElement | type: FElement | - | This function adds the input element into **children** and set the **parentElement** of the input element |
| removeElement | type: FElement *(child=None)* | - | This function removes the input element in **children** |
| setAttrTag | - | type: str | This function returns customizing attributes of the corresponding html tag in html string format |
| addStaticScript | type: FElement | - | This function adds the input element into **script** |
| removeStaticScript | type: FElement *(script=None)* | - | This function removes the input element in **script** |
| render_inner | - | type: str | This function returns the return value of the function **render_element** and extend its **script** list to its parent's **script** list |
| render_script | - | type: str | This function returns the all static scripts in a pure html format |
| render_element | - | type: str | This function renders the element and returns its pure html script |

<br>
### Support Elements
**html tag**: *tag which is supported by html*<br>
`a, button, div, form, h1, h2, h3, h4, h5, h6, iframe, img, input, label, li, ol, option, p, script, style, table, textarea`<br>
<br>
**Famcy tag**: *a new tag which is design by Famcy*<br>
`ELEMENT (Tag concatenated elements)`<br>
<br>
### Create a New FElement
To create a new FElement, make sure each element inherits Famcy.FamcyElement and contains the render function `render_element` which returns pure html string. The following shows an example:
<br>

	import Famcy
	class new_element(Famcy.FamcyElement):
    	def __init__(self):
        	super(new_element, self).__init__()
	
    	def render_element(self):
        	return ***html string***
<br>

To return html string of children elements and generate their html attributes when running `render_element`, the following is the example.
<br>

	def render_element(self):
        html = ""

        if self.innerHTML and self.innerHTML != "":
            html += self.innerHTML
            self.children = []
        else:
            for child in self.children:
                html += child.render_inner()
                child.parentElement = self
        self.html = html
        return "<div" + self.setAttrTag() + ">" + html + "</div>"
