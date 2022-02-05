# Famcy Items
This goes through how to develop your customized famcy items and the natively provided famcy item templates.<br>
Famcy provides multiple FBlock and FCard templates for the development of the front end web. The following is the chart of different type of FBlock which Famcy provides and the items that Famcy includes as well as some examples of the usage of these Famcy items. This documentation also includes the examples of adding FBlock into FCard layout in code.<br>
<br>

## FBlock
### FBlock templates

| Class Name | Parent Class | Definition |
| ---------- | ------------ | ---------- |
| FBlock | FamcyWidget | This is the parent class of a item that is a combination of FElements and can be placed in FCard |
| FInputBlock | FBlock | This is the parent class of a item that the user can edit or get the value of it. The child class of FInputBlock requires the user to provide "action_after_post" and "mandatory" keys |
| FUploadBlock | FBlock | This is the parent class of a item when the user needs to upload of download file |

### Create a custom FBlock
To create a custom FBlock item, make sure each element inherits Famcy.FamcyBlock and contains `init_block`, `generate_template_content` and `render_inner` which returns FElement. The following is an example of a custom FBlock item:<br>
<br>

	import Famcy
	class fblock_item(Famcy.FamcyBlock):
    	def __init__(self):
        	self.value = fblock_item.generate_template_content()
        	super(fblock_item, self).__init__()
        	self.init_block()
	
    	@classmethod
    	def generate_template_content(cls):
    		"""
    		This function returns values that the user can edit in Famcy.
    		"""
        	return {
            	"h1": "",
            	"h2": ""
        	}
	
    	def init_block(self):
    		"""
    		This function create the html structure of the item by using FElements
    		"""
        	self.body = Famcy.div()
        	self.body["id"] = self.id
        	self.body["className"] = "fblock_item"
	
        	h1_temp = Famcy.h1()
        	h2_temp = Famcy.h2()
	
        	self.body.addElement(h1_temp)
        	self.body.addElement(h2_temp)
	
    	def render_inner(self):
    		"""
    		This function updates values that the user edited
    		"""
    		self.body.children[0].innerHTML = self.value["h1"]
    		self.body.children[1].innerHTML = self.value["h2"]
	
        	return self.body

<br>

### FBlock items provided by Famcy

| Class Name 				| Submittable Item 	| Values 											|
| ------------------------- | ----------------- | ------------------------------------------------- |
| bar_chart 				| x					| values<br>labels<br>title<br>xy_axis_title<br>size |										
| line_chart 				| x					| values<br>labels<br>title |
| pie_chart 				| x					| values<br>labels<br>size |
| event_calendar 			| x					| language<br>events |
| with_btn_calendar 		| v					| title<br>mandatory<br>action_after_post<br>weekdays<br>months<br>week_avail<br>special_avail_dict |
| table_block 				| v					| input_button<br>input_value_col_field<br>page_detail<br>page_detail_content<br>toolbar<br>page_footer<br>page_footer_detail<br>column<br>data |
| video_stream 				| x					| refreash_stream<br>stop_stream<br>title<br>desc<br>rtsp_address<br>video_timeout<br>holder_width<br>holder_height<br>img_path |
| displayImage 				| x					| title<br>img_name<br>img_size<br>border_radius |
| displayLight 				| x					| title<br>status<br>light_size |
| displayParagraph 			| x					| title<br>content |
| displayPicWord 			| x					| title<br>content<br>img_src |
| displayStepLoader 		| x					| title<br>steps<br>steps_status |
| displayTag 				| x					| title<br>content |
| inputBlockSec 			| v					| title<br>content<br>img_src<br>btn_name |
| inputBtn 					| v					| title<br>desc<br>input_type<br>num_range<br>placeholder<br>mandatory<br>button_name<br>action_after_post |
| inputList 				| v					| title<br>desc<br>mandatory<br>value<br>action_after_post |
| inputParagraph 			| v					| title<br>desc<br>height<br>placeholder<br>mandatory<br>action_after_post |
| inputPassword 			| v					| title<br>desc<br>mandatory<br>action_after_post |
| multipleChoicesRadioInput | v					| title<br>desc<br>mandatory<br>value<br>action_after_post |
| pureInput 				| v					| title<br>desc<br>defaultValue<br>input_type<br>num_range<br>placeholder<br>mandatory<br>action_after_post |
| singleChoiceRadioInput 	| v					| title<br>desc<br>mandatory<br>value<br>action_after_post |
| submitBtn 				| v					| title<br>mandatory<br>action_after_post |
| urlBtn 					| v					| title<br>style<br>url<br>desc<br>mandatory<br>button_name<br>action_after_post |
| downloadFile 				| v					| title<br>file_path<br>file_name<br>mandatory<br>action_after_post |
| uploadFile 				| v					| title<br>file_num<br>accept_type<br>file_path<br>mandatory<br>action_after_post |


<br>

### Create a New FBlock
This is a example of creating a FBlock item and setting some details of the block.<br>
<br>

	block = Famcy.displayTag()
	block.update({
                "title": "Title",
                "content": "Content"
            })

<br>
The following shows the example of creating a FInputBlock item and connect the block item with a submission function.<br>
<br>
	
	iblock = Famcy.pureInput()
    iblock.update({"title": "Input Block"})
    iblock.connect(python_action, target=card)

<br>

## FCard
### FCard templates

| Class Name | Parent Class | Definition |
| ---------- | ------------ | ---------- |
| FCard | FamcyWidget | This is a card holder that can place a lot of FBlock(widget) in it |
| FPromptCard | FCard | This is a pop up card holder |
| input_form | FCard | This is a input form holder that can submit input information |
| upload_form | FCard | This is a upload form holder that can upload the file and get value of it |

<br>

### Create a New FCard
This is a example of creating a FCard and setting the title of the card.<br>
<br>

	card = Famcy.FamcyCard()
	card.title = "FCard Example"

<br>
The following shows the example of adding multiple FBlocks in FCard. Using the action `addWidget` to add fblock into the card layout. `addWidget` needs parameter `addWidget(row number, column number, height [default=1], width [default=1])`<br>
<br>
	
	card = Famcy.FamcyCard()
	card.layout.addWidget(fblock1, 0, 0)

<br>
The followings are the example of creating FPromptCard, input_form and upload_form.<br>
<br>

	pcard = Famcy.FamcyPromptCard()
	pcard.layout.addWidget(fblock1, 0, 0)

	icard = Famcy.input_form()
	icard.layout.addWidget(fblock2, 0, 0)

	ucard = Famcy.upload_form()
	ucard.layout.addWidget(fblock3, 0, 0)

<br>

