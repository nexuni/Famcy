import json
import Famcy
import markdown
# from PostgreSQL.schema import *
# from PostgreSQL.robot_meta_info import *
import requests

ROBOT_ID="test"
ROBOT_META_INFO_DATA="test_info"
CANVAS_W = 525
CANVAS_H = 600

class canvas_block(Famcy.FamcyBlock):

    def __init__(self, **kwargs):
        self.value = canvas_block.generate_template_content()
        super(canvas_block, self).__init__(**kwargs)
        self.init_block()

    @classmethod
    def generate_template_content(cls, fblock_type=None):
        return {
            ROBOT_ID: "",
            ROBOT_META_INFO_DATA: {},
            "route": [{
                "key_name": "route_1",
                "points": [],
                "pos": {"x": 0, "y": 0},
                "more_info": {"width": 5, "color": "blue"}
            }],
            "area_key_name": "route_1"
        }

    def init_block(self):
        self.body = Famcy.div()
        self.body["id"] = self.id
        self.body["className"] = "canvas_block"

        gimg_holder = Famcy.div()
        gimg_holder["id"] = "canvasHolder"

        gimg = Famcy.img()
        gimg["id"] = "imgCanvasMap"
        gimg_holder.addElement(gimg)

        gimg_mask = Famcy.div()
        gimg_mask["id"] = "imgCanvasMapMask"
        gimg_holder.addElement(gimg_mask)

        self.body.addElement(gimg_holder)

        script = Famcy.script()
        self.body.addElement(script)

        self.areaBtn = Famcy.button()
        self.areaBtn["className"] = "small_submit_btn"
        self.areaBtn["id"] = "btnAddRect"
        self.areaBtn.innerHTML = "add rect"
        self.body.addElement(self.areaBtn)

        self.sendInfoBtn = Famcy.button()
        self.sendInfoBtn["className"] = "small_submit_btn"
        self.sendInfoBtn["id"] = "btnRectInfo"
        self.sendInfoBtn.innerHTML = "rect info"
        self.body.addElement(self.sendInfoBtn)

        self.gsavebtn = Famcy.button()
        self.gsavebtn["className"] = "small_submit_btn"
        self.gsavebtn["id"] = "btnCanvasSave"
        self.gsavebtn.innerHTML = "save"
        self.body.addElement(self.gsavebtn)

        self.clearBtn = Famcy.button()
        self.clearBtn["className"] = "small_submit_btn"
        self.clearBtn["id"] = "btnClear"
        self.clearBtn.innerHTML = "clear"
        self.body.addElement(self.clearBtn)

        my_script = Famcy.script()
        my_script["src"] = "asset/js/canvas_handler.js"
        self.body.addStaticScript(my_script, position="head")

        static_style = Famcy.style()
        static_style.innerHTML = """
            #canvasHolder {
                position: relative;
                width: %spx;
                height: %spx;
            }

            #imgCanvasMap {
                width: %spx;
                height: %spx;
            }

            #imgCanvasMapMask {
                position: absolute;
                top: 0;
                left: 0;
                width: %spx;
                height: %spx;
            }
        """ % (str(CANVAS_W), str(CANVAS_H), str(CANVAS_W), str(CANVAS_H), str(CANVAS_W), str(CANVAS_H))
        self.body.addStaticScript(static_style, position="head") 

        konva_script = Famcy.script()
        konva_script["src"] = "https://unpkg.com/konva@8.3.5/konva.min.js"
        self.body.addStaticScript(konva_script, position="head")

    def update_route(self, key_name, points, pos, more_info):
        print("update_route")
        Famcy.sse.publish({
            "indicator": True,
            "more_info": json.dumps(more_info),
            "key_name": key_name,
            "points": json.dumps(points),
            "pos": json.dumps(pos)
            },
            type='canvas_block')

    def render_inner(self):
        robot_pos = {
                "lat": 19.0883595,
                "lng": 72.82652380000002,
            }

        self.clearBtn["onclick"] = f"c_clearRoute()"
        self.areaBtn["onclick"] = f"c_addRect('{self.submission_obj_key}')"
        self.sendInfoBtn["onclick"] = "c_sendRectInfo('%s', '%s')" % (self.submission_obj_key, self.value["area_key_name"])
        self.gsavebtn["onclick"] = f"c_saveRoute('{self.value[ROBOT_ID]}', '{self.name}','{self.submission_obj_key}')"
        # self.body.children[1].innerHTML = \
        #     f"Draw_pic(\
        #         {json.dumps(self.value[ROBOT_ID])},\
        #             {json.dumps(self.value['route'])},\
        #                 {json.dumps(self.value[ROBOT_META_INFO_DATA])});"
        self.body.children[1].innerHTML = \
            f"Draw_pic(\
                {json.dumps(self.value[ROBOT_ID])},\
                    {json.dumps(self.value['route'])},\
                        {CANVAS_W},\
                            {CANVAS_H});"

        return self.body