import Famcy
import json

class joyStick(Famcy.FamcyBlock):
    """
    Represents the block to display
    paragraph. 
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.callback = None
        self.value = joyStick.generate_template_content()
        super(joyStick, self).__init__()
        self.init_block()

    @classmethod
    def generate_template_content(cls):
        return {
            
        }

    def init_block(self):
        self.body = Famcy.div()
        self.body["id"] = self.id
        self.body["className"] = "joyDiv"

        _joyStick = Famcy.div()
        _joyStick["id"] = self.id+"_joyDiv"

        _script = Famcy.script()
        _script.innerHTML = '''
        var joy = new JoyStick('%s', '%s',{

            // The ID of canvas element
            title: 'joystick',

            // width/height
            width: '100',
            height: '100',

            // Internal color of Stick
            internalFillColor: '#00AA00',

            // Border width of Stick
            internalLineWidth: 2,

            // Border color of Stick
            internalStrokeColor: '#003300',

            // External reference circonference width
            externalLineWidth: 2,

            //External reference circonference color
            externalStrokeColor: '#008000',
            
            // Sets the behavior of the stick
            autoReturnToCenter: true
            
        });
        ''' % (self.id+"_joyDiv", self.submission_obj_key)

        self.body.addElement(_joyStick)
        self.body.addElement(_script)

        _static_script = Famcy.script()
        _static_script["src"] = "/asset/js/joy.js"
        self.body.addStaticScript(_static_script, position="head")

    def js_callback(self, s_obj, info):
        print(info.raw_data)
        self.x = info.raw_data["x"]
        self.y = info.raw_data["y"]
        if self.callback:
            self.callback()
        return Famcy.UpdateNothing()

    def render_inner(self):

        self.connect(self.js_callback)
        self.clickable = False
        
        return self.body
