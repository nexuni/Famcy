import json
import Famcy
import markdown
import requests

# [24.98728136, 121.55250466]

GOOGLE_MAP_W = 525
GOOGLE_MAP_H = 600

class google_map(Famcy.FamcyBlock):

    def __init__(self, **kwargs):
        self.value = google_map.generate_template_content()
        super(google_map, self).__init__(**kwargs)
        self.init_block()

    @classmethod
    def generate_template_content(cls, fblock_type=None):
        return {
            "robot_id": "",
            # "anomaly_pos": {},
            "route": [{
                "key_name": "route_1",
                "points": [1, 2, 3, 4, 5, 60],
                "pos": {"x": 0, "y": 0}, # ????????
                "more_info": {"width": 5, "color": "blue"}
            }],
            # "center": [24.98728136, 121.55250466],
            "zoom": 18,
            # "map_flag": True,
            # "load_img": True
        }

    def init_block(self):
        self.body = Famcy.div()
        self.body["id"] = self.id
        self.body["className"] = "google_map"

        gmap = Famcy.div()
        gmap["id"] = "map"
        gmap.style["position"] = "relative"
        gmap.style["overflow"] = "hidden"
        self.body.addElement(gmap)
        script = Famcy.script()
        self.body.addElement(script)

        # ??????
        gimg_holder = Famcy.div()
        gimg_holder["id"] = "imgMapHolder"
        gimg_holder.style["display"] = "none"
        
        # ??????
        gimg = Famcy.div()
        gimg["id"] = "imgMap"
        gimg_holder.addElement(gimg)
        
        # ??????
        gimg_mask = Famcy.div()
        gimg_mask["id"] = "imgMapMask"
        gimg_holder.addElement(gimg_mask)

        self.body.addElement(gimg_holder)

        # submit button
        gbtn = Famcy.button()
        gbtn["className"] = "small_submit_btn"
        gbtn["id"] = "btnExport"
        gbtn["onclick"] = f"takeshot('{GOOGLE_MAP_W}', '{GOOGLE_MAP_H}', '{self.submission_obj_key}')"
        gbtn.innerHTML = "Snapshot"
        self.body.addElement(gbtn)

        # download button
        gdownloadbtn = Famcy.a()
        gdownloadbtn["className"] = "small_submit_btn"
        gdownloadbtn["id"] = "btnDownload"
        gdownloadbtn["onclick"] = "download_img()"
        gdownloadbtn["download"] = "gmap.png"
        gdownloadbtn.innerHTML = "download"
        # self.body.addElement(gdownloadbtn)

        # save button
        self.reset_cookie = Famcy.button()
        self.reset_cookie["className"] = "small_submit_btn"
        # self.reset_cookie["id"] = "btnSave"
        self.reset_cookie["onclick"] = "clearRoute();"
        self.reset_cookie.innerHTML = "reset"
        self.body.addElement(self.reset_cookie)


        my_script = Famcy.script()
        my_script["src"] = "asset/js/google_map_handler.js"
        self.body.addStaticScript(my_script, position="head")

        static_style = Famcy.style()
        static_style.innerHTML = """
            #map {
                width: %spx;
                height: %spx;
            }

            #imgMapHolder {
                position: relative;
                width: %spx;
                height: %spx;
            }

            #imgMapMask {
                position: absolute;
                top: 0;
                left: 0;
                width: %spx;
                height: %spx;
            }
        """ % (str(GOOGLE_MAP_W), str(GOOGLE_MAP_H), str(GOOGLE_MAP_W), str(GOOGLE_MAP_H), str(GOOGLE_MAP_W), str(GOOGLE_MAP_H))
        self.body.addStaticScript(static_style, position="head") 

        map_script = Famcy.script()
        map_script["src"] = "https://maps.googleapis.com/maps/api/js?key="+Famcy.FManager["ConsoleConfig"]["google_map"]
        self.body.addStaticScript(map_script, position="head")

        html2canvas_script = Famcy.script()
        html2canvas_script["src"] = "https://cdn.jsdelivr.net/npm/html2canvas@1.0.0-rc.5/dist/html2canvas.min.js"
        self.body.addStaticScript(html2canvas_script, position="head")

        konva_script = Famcy.script()
        konva_script["src"] = "https://unpkg.com/konva@8.3.5/konva.min.js"
        self.body.addStaticScript(konva_script, position="head")

    def update_route(self, key_name, points, pos, more_info):
        Famcy.sse.publish({
            "indicator": True,
            "more_info": json.dumps(more_info),
            "key_name": key_name,
            "points": json.dumps(points),
            "pos": json.dumps(pos)},
            type='publish',
            channel="event_source._gmap_"
            )

    def render_inner(self):
        robot_pos = {
                "lat": 19.0883595,
                "lng": 72.82652380000002,
            }


        self.body.children[1].innerHTML = \
            f"Draw_google_map(\
                {json.dumps(robot_pos)},\
                    {json.dumps(self.value['route'])},\
                        {self.value['zoom']},\
                            {json.dumps(self.value['robot_id'])});"
        return self.body