var C_ROUTE_DICT={};
var C_AREA_DICT={};
var C_LINE_DICT={};
var C_RECT_DICT={};
var C_CANVAS_FLAG=false;
var C_CANVAS;
var default_area_w=525*8/20, default_area_h=525/2;

var source = new EventSource("/event_source?channel=event_source._canvas_");
source.addEventListener('publish', function(event) {
    var data = JSON.parse(event.data);
    c_drawFBlockRoute(data.key_name, JSON.parse(data.points), JSON.parse(data.pos), JSON.parse(data.more_info))
    c_add_all_route_to_canvas()
}, false);
source.addEventListener('error', function(event) {
    console.log("Error"+ event)
}, false);

function Draw_pic(
    robot_id,
    route_info,
    w=525, h=600, load_db=false) {
    
    c_loadImage()
    if (load_db) {
        C_LINE_DICT = c_loadDb(robot_id, load)
        C_RECT_DICT = {} // TODO
        C_ROUTE_DICT={}
        C_AREA_DICT={}
        C_CANVAS = c_init_canvas('imgCanvasMapMask', w, h)
        C_CANVAS_FLAG = true
    }
    else {
        C_LINE_DICT = c_loadRoute()
        C_RECT_DICT = c_loadArea()
        C_ROUTE_DICT={}
        C_AREA_DICT={}
        C_CANVAS = c_init_canvas('imgCanvasMapMask', w, h)
        C_CANVAS_FLAG = true

        load()
    }


    function load () {
        c_drawStorageRoute()
        c_drawStorageArea()

        for (var i = 0; i < route_info.length; i++) {
            c_drawFBlockRoute(route_info[i].key_name, route_info[i].points, route_info[i].pos, route_info[i].more_info)
        }
        
        c_add_all_route_to_canvas()
        c_add_all_area_to_canvas()
    }
}

function c_add_all_route_to_canvas() {
    if (C_CANVAS_FLAG) {
        for (var i = 0; i < Object.keys(C_ROUTE_DICT).length; i++) {
            C_CANVAS.add(C_ROUTE_DICT[Object.keys(C_ROUTE_DICT)[i]]["layer"])
        }
    }
}

function c_add_all_area_to_canvas() {
    if (C_CANVAS_FLAG) {
        for (var i = 0; i < Object.keys(C_AREA_DICT).length; i++) {
            C_CANVAS.add(C_AREA_DICT[Object.keys(C_AREA_DICT)[i]]["layer"])
        }
    }
}

function c_remove_all_route_to_canvas() {
    if (C_CANVAS_FLAG) {
        for (var i = 0; i < Object.keys(C_ROUTE_DICT).length; i++) {
            C_ROUTE_DICT[Object.keys(C_ROUTE_DICT)[i]]["layer"].removeChildren()
        }
    }
}

function c_remove_all_area_to_canvas() {
    if (C_CANVAS_FLAG) {
        for (var i = 0; i < Object.keys(C_AREA_DICT).length; i++) {
            C_AREA_DICT[Object.keys(C_AREA_DICT)[i]]["layer"].removeChildren()
        }
    }
}

function c_loadImage() {
    const img = getSavedValue("imageData")
    document.getElementById("imgCanvasMap").setAttribute('src', img);
}

function c_loadRoute() {
    // get route from local storage
    var temp
    if (getSavedValue("lineDict") === "") {
        temp = {}
    }
    else {
        temp = JSON.parse(getSavedValue("lineDict"))
    }
    for (var i = 0; i < Object.keys(temp).length; i++) {
        temp[Object.keys(temp)[i]]["line"] = false
        temp[Object.keys(temp)[i]]["layer"] = false
    }
    return temp
}

function c_loadArea() {
    // get route from local storage
    var temp
    if (getSavedValue("rectDict") === "") {
        temp = {}
    }
    else {
        temp = JSON.parse(getSavedValue("rectDict"))
    }
    for (var i = 0; i < Object.keys(temp).length; i++) {
        temp[Object.keys(temp)[i]]["rect"] = false
        temp[Object.keys(temp)[i]]["text"] = false
        temp[Object.keys(temp)[i]]["layer"] = false
    }
    return temp
}

function c_addRect(obj_key) {
    let res_dict = {}
    let token = document.head.querySelector("[name~=csrf-token][content]").content;
    Sijax.request('famcy_submission_handler', [obj_key, res_dict], { data: { csrf_token: token } });
}

function c_sendRectInfo(obj_key, line_name) {
    let res_dict = {}

    let ox = C_LINE_DICT[line_name]["line_attr"]["x"] ? C_LINE_DICT[line_name]["line_attr"]["x"] : 0
    let oy = C_LINE_DICT[line_name]["line_attr"]["y"] ? C_LINE_DICT[line_name]["line_attr"]["y"] : 0
    let osx = C_LINE_DICT[line_name]["line_attr"]["scaleX"] ? C_LINE_DICT[line_name]["line_attr"]["scaleX"] : 1
    let osy = C_LINE_DICT[line_name]["line_attr"]["scaleY"] ? C_LINE_DICT[line_name]["line_attr"]["scaleY"] : 1
    let or = C_LINE_DICT[line_name]["line_attr"]["rotation"] ? C_LINE_DICT[line_name]["line_attr"]["rotation"] : 0

    for (var i = 0; i < Object.keys(C_RECT_DICT).length; i++) {
        let rx = C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["group_attr"]["x"] ? C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["group_attr"]["x"] : 0
        let ry = C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["group_attr"]["y"] ? C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["group_attr"]["y"] : 0
        let rsx = C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["group_attr"]["scaleX"] ? C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["group_attr"]["scaleX"] : 1
        let rsy = C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["group_attr"]["scaleY"] ? C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["group_attr"]["scaleY"] : 1
        let rr = C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["group_attr"]["rotation"] ? C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["group_attr"]["rotation"] : 0

        let dx = rx;
        let dy = ry;
        let dsx = rsx;
        let dsy = rsy;
        let dr = rr;

        res_dict[Object.keys(C_RECT_DICT)[i]] = {
            "p1": [dx, dy],
            "p2": [dx-Math.sin(Math.PI*(dr/180))*default_area_h*dsy, dy+Math.cos(Math.PI*(dr/180))*default_area_h*dsy],
            "p3": [dx+Math.cos(Math.PI*(dr/180))*default_area_w*dsx-Math.sin(Math.PI*(dr/180))*default_area_h*dsy, dy+Math.sin(Math.PI*(dr/180))*default_area_w*dsx+Math.cos(Math.PI*(dr/180))*default_area_h*dsy],
            "p4": [dx+Math.cos(Math.PI*(dr/180))*default_area_w*dsx, dy+Math.sin(Math.PI*(dr/180))*default_area_w*dsx],
        }
    }

    res_dict["origin"] = {
        "x": oy,
        "y": ox,
        "scaleX": osy,
        "scaleY": osx,
        "rotation": Math.PI*(or/180),
    }
    console.log(res_dict)

    let token = document.head.querySelector("[name~=csrf-token][content]").content;
    Sijax.request('famcy_submission_handler', [obj_key, res_dict], { data: { csrf_token: token } });
}

function c_showRect(name, color) {
    let rect1 = new Konva.Rect({
        x: 0,
        y: 0,
        width: default_area_w,
        height: default_area_h,
        fill: color,
        name: "rect",
        opacity: 0.3,
    });

    let simpleText = new Konva.Text({
        x: 5,
        y: 5,
        text: name,
        fontSize: 15,
        fontFamily: 'Calibri',
        fill: color,
        name: "text"
    });

    let group = new Konva.Group({
        draggable: true,
    });
    var layer = new Konva.Layer();
    group.add(rect1);
    group.add(simpleText);
    layer.add(group);
    layer.draw();

    C_AREA_DICT[name] = {}
    C_AREA_DICT[name]["rect"] = rect1
    C_AREA_DICT[name]["text"] = simpleText
    C_AREA_DICT[name]["layer"] = layer

    C_RECT_DICT[name] = {}
    C_RECT_DICT[name]["group_attr"] = group["attrs"]
    C_RECT_DICT[name]["rect_attr"] = rect1["attrs"]
    C_RECT_DICT[name]["text_attr"] = simpleText["attrs"]

    C_CANVAS.add(layer)

    saveValue("rectDict", JSON.stringify(C_RECT_DICT))
}

function c_drawFBlockRoute(key_name, points, pos, more_info={"width": 8, "color": "red"}) {
    if (!Object.keys(C_LINE_DICT).includes(key_name)) {
        let line = new Konva.Line({
            x: pos["x"],
            y: pos["y"],
            id: key_name,
            points: points,
            stroke: more_info["color"],
            strokeWidth: more_info["width"],
            lineCap: 'round',
            lineJoin: 'round',
            // tension: 1,
            draggable: true,
        });

        let layer = new Konva.Layer();
        layer.add(line);
        layer.draw();
        C_ROUTE_DICT[key_name] = {}
        C_ROUTE_DICT[key_name]["line"] = line
        C_ROUTE_DICT[key_name]["layer"] = layer

        C_LINE_DICT[key_name] = {}
        C_LINE_DICT[key_name]["line_attr"] = line["attrs"]
    }
    else if (Object.keys(C_ROUTE_DICT).includes(key_name)) {
        let line = C_ROUTE_DICT[key_name]["line"]
        let layer = C_ROUTE_DICT[key_name]["layer"]
        line["attrs"]["points"] = points
        layer.draw()
    }
    else {
        let line = new Konva.Line(C_LINE_DICT[key_name]["line_attr"]);

        let layer = new Konva.Layer();
        layer.add(line);
        layer.draw();
        C_ROUTE_DICT[key_name] = {}
        C_ROUTE_DICT[key_name]["line"] = line
        C_ROUTE_DICT[key_name]["layer"] = layer
    }
}

function c_drawStorageRoute() {
    for (var i = 0; i < Object.keys(C_LINE_DICT).length; i++) {
        if(!Object.keys(C_ROUTE_DICT).includes(Object.keys(C_LINE_DICT)[i])) {
            let line = new Konva.Line(C_LINE_DICT[Object.keys(C_LINE_DICT)[i]]["line_attr"]);

            let layer = new Konva.Layer();
            layer.add(line);
            layer.draw();
            C_ROUTE_DICT[Object.keys(C_LINE_DICT)[i]] = {}
            C_ROUTE_DICT[Object.keys(C_LINE_DICT)[i]]["line"] = line
            C_ROUTE_DICT[Object.keys(C_LINE_DICT)[i]]["layer"] = layer
        }
    }
}

function c_drawStorageArea() {
    for (var i = 0; i < Object.keys(C_RECT_DICT).length; i++) {
        let rect1 = new Konva.Rect(C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["rect_attr"]);

        let simpleText = new Konva.Text(C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["text_attr"]);

        let group = new Konva.Group(C_RECT_DICT[Object.keys(C_RECT_DICT)[i]]["group_attr"]);
        let layer = new Konva.Layer();
        group.add(rect1);
        group.add(simpleText);
        layer.add(group);
        layer.draw();
        C_AREA_DICT[Object.keys(C_RECT_DICT)[i]] = {}
        C_AREA_DICT[Object.keys(C_RECT_DICT)[i]]["rect"] = rect1
        C_AREA_DICT[Object.keys(C_RECT_DICT)[i]]["text"] = simpleText
        C_AREA_DICT[Object.keys(C_RECT_DICT)[i]]["layer"] = layer
        
    }
}


function c_init_canvas(key, w, h) {
    let width = w;
    let height = h;

    var stage = new Konva.Stage({
        container: key,
        width: width,
        height: height,
    });

    var layer = new Konva.Layer();
    stage.add(layer);

    var tr = new Konva.Transformer();
    layer.add(tr);

    // add a new feature, lets add ability to draw selection rectangle
    var selectionRectangle = new Konva.Rect({
        fill: 'rgba(0,0,255,0.5)',
        visible: false,
    });
    layer.add(selectionRectangle);

    var x1, y1, x2, y2, key_name, line;
    stage.on('mousedown touchstart', (e) => {
        // do nothing if we mousedown on any shape
        if (e.target !== stage) {
            return;
        }

        // key_name = e.target.attrs.id
        // console.log("touchstart", e.target, e.target.attrs.id)

        e.evt.preventDefault();
        x1 = stage.getPointerPosition().x;
        y1 = stage.getPointerPosition().y;
        x2 = stage.getPointerPosition().x;
        y2 = stage.getPointerPosition().y;

        selectionRectangle.visible(true);
        selectionRectangle.width(0);
        selectionRectangle.height(0);
    });

    stage.on('mousemove touchmove', (e) => {
        // do nothing if we didn't start selection
        if (!selectionRectangle.visible()) {
          return;
        }
        e.evt.preventDefault();
        x2 = stage.getPointerPosition().x;
        y2 = stage.getPointerPosition().y;

        selectionRectangle.setAttrs({
          x: Math.min(x1, x2),
          y: Math.min(y1, y2),
          width: Math.abs(x2 - x1),
          height: Math.abs(y2 - y1),
        });

    });

    stage.on('mouseup touchend', (e) => {
        for (var i = 0; i < Object.keys(C_ROUTE_DICT).length; i++) {
            key_name = Object.keys(C_ROUTE_DICT)[i]
            line = C_ROUTE_DICT[key_name]["line"]
            // update line dict data
            C_LINE_DICT[key_name]["line_attr"] = line["attrs"]
        }

        for (var i = 0; i < Object.keys(C_AREA_DICT).length; i++) {
            key_name = Object.keys(C_AREA_DICT)[i]
            rect = C_AREA_DICT[key_name]["rect"]
            text = C_AREA_DICT[key_name]["text"]
            // update line dict data
            C_RECT_DICT[key_name]["rect_attr"] = rect["attrs"]
            C_RECT_DICT[key_name]["text_attr"] = text["attrs"]
            C_RECT_DICT[key_name]["group_attr"] = rect.parent["attrs"]
        }

        saveValue("lineDict", JSON.stringify(C_LINE_DICT))
        saveValue("rectDict", JSON.stringify(C_RECT_DICT))

        // do nothing if we didn't start selection
        if (!selectionRectangle.visible()) {
          return;
        }
        e.evt.preventDefault();
        // update visibility in timeout, so we can check it in click event
        setTimeout(() => {
          selectionRectangle.visible(false);
        });

        var shapes = stage.find('.line');
        var box = selectionRectangle.getClientRect();
        var selected = shapes.filter((shape) =>
          Konva.Util.haveIntersection(box, shape.getClientRect())
        );
        tr.nodes(selected);
    });

    // clicks should select/deselect shapes
    stage.on('click tap', function (e) {
        // if we are selecting with rect, do nothing
        if (selectionRectangle.visible()) {
          return;
        }

        // if click on empty area - remove all selections
        if (e.target === stage) {
          tr.nodes([]);
          return;
        }

        // do nothing if clicked NOT on our rectangles
        if (e.target.hasName('rect') || e.target.hasName('text')) {
            var parentGroups = e.target.parent;
            var _target = parentGroups
            console.log(parentGroups)
        }
        else {
            var _target = e.target
        }

        // do we pressed shift or ctrl?
        const metaPressed = e.evt.shiftKey || e.evt.ctrlKey || e.evt.metaKey;
        const isSelected = tr.nodes().indexOf(_target) >= 0;

        if (!metaPressed && !isSelected) {
          // if no key pressed and the node is not selected
          // select just one
          tr.nodes([_target]);
        } else if (metaPressed && isSelected) {
          // if we pressed keys and node was selected
          // we need to remove it from selection:
          const nodes = tr.nodes().slice(); // use slice to have new copy of array
          // remove node from array
          nodes.splice(nodes.indexOf(_target), 1);
          tr.nodes(nodes);
        } else if (metaPressed && !isSelected) {
          // add the node into selection
          const nodes = tr.nodes().concat([_target]);
          tr.nodes(nodes);
        }
    });


    return stage
}


function c_loadDb (robot_id, callback) {
    console.log("c_loadDb")
    // load db
    let url = ""
    let res_dict = {
        "service": "robot_meta_info", 
        "operation": "get_google_map_settings", 
        "robot_id": robot_id
    }
    let res_str = dict2urlEncode(res_dict)
    
    getDataFromServer(url+"?"+res_str)
        .then(res => {
            let img_data = res["img_data"]
            let line_data = res["line_data"]
            saveValue("imageData", res["img_data"])
            saveValue("lineDict", line_data)
        })
        .then(() => {
            callback()
        })
}
function c_saveRoute(robot_id) {
    // call API to save data
    saveValue("imageData", document.getElementById("imgCanvasMap").getAttribute('src'))
    saveValue("lineDict", JSON.stringify(C_LINE_DICT))
    saveValue("rectDict", JSON.stringify(C_RECT_DICT))
    const img_data = document.getElementById("imgCanvasMap").getAttribute('src');
    const line_data = C_LINE_DICT;

    let url = ""
    let res_dict = {
        "service": "robot_meta_info", 
        "operation": "add_google_map_settings", 
        "robot_id": robot_id, 
        "route_data": {
            "img_data": img_data,
            "route_dict": line_data
        }
    }
    let res_str = JSON.stringify(res_dict)

    postDataFromServer(url, res_str)
        .then(res => {
            console.log("save data")
        })

}

function c_clearRoute() {
    C_LINE_DICT = {}
    C_RECT_DICT = {}
    saveValue("imageData", "")
    saveValue("lineDict", JSON.stringify(C_LINE_DICT))
    saveValue("rectDict", JSON.stringify(C_RECT_DICT))

    c_remove_all_route_to_canvas()
    c_remove_all_area_to_canvas()
}