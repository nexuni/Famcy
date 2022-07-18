var ROUTE_DICT={};
var LINE_DICT={};
var CANVAS_FLAG=false;
var CANVAS, CANVAS_HTML;

source.addEventListener('gmap', function(event) {
    var data = JSON.parse(event.data);
    drawFBlockRoute(data.key_name, JSON.parse(data.points), JSON.parse(data.pos), JSON.parse(data.more_info))
    add_all_route_to_canvas()
}, false);

function Draw_google_map(
    robot_pos,
    route_info,
    zoom=18, robot_id="", load_db=false) {
    /*
    API Reference: https://developers.google.com/maps/documentation/javascript/reference
    */

    // init variable
    ROUTE_DICT={}
    CANVAS_FLAG=false
    

    if (load_db) {
        LINE_DICT = loadDb(robot_id, load)
    }
    else {
        LINE_DICT = loadRoute()
        load()
    }


    function load() {
        // draw map
        var mapOptions = {
            center: robot_pos,
            zoom: zoom,                 // 0 ~ 22
            streetViewControl: false,   // Street view UI at bottom right (with a yellow human icon)
            keyboardShortcuts: false,   // Keyboard short cut to interact with map (zooming, panning, ...)
            fullscreenControl: false,   // Full screen UI at top right
            clickableIcons: false,      // The icon on the map
            mapTypeControl: false,
            mapTypeId: 'roadmap'
        }
        const map = new google.maps.Map(document.getElementById("map"), mapOptions);

        // draw route
        for (var i = 0; i < route_info.length; i++) {
            drawFBlockRoute(route_info[i].key_name, route_info[i].points, route_info[i].pos, route_info[i].more_info)
        }

        drawStorageRoute()
    }
}

function drawFBlockRoute(key_name, points, pos, more_info={"width": 8, "color": "red"}) {
    if (!Object.keys(LINE_DICT).includes(key_name)) {
        let line = new Konva.Line({
            x: pos["x"],
            y: pos["y"],
            id: key_name,
            points: points,
            stroke: more_info["color"],
            strokeWidth: more_info["width"],
            lineCap: 'round',
            lineJoin: 'round',
            tension: 1,
            draggable: true,
        });

        let layer = new Konva.Layer();
        layer.add(line);
        layer.draw();
        ROUTE_DICT[key_name] = {}
        ROUTE_DICT[key_name]["line"] = line
        ROUTE_DICT[key_name]["layer"] = layer

        LINE_DICT[key_name] = {}
        LINE_DICT[key_name]["line_attr"] = line["attrs"]
    }
    else if (Object.keys(ROUTE_DICT).includes(key_name)) {
        let line = ROUTE_DICT[key_name]["line"]
        let layer = ROUTE_DICT[key_name]["layer"]
        line["attrs"]["points"] = points
        layer.draw()
    }
    else {
        let line = new Konva.Line(LINE_DICT[key_name]["line_attr"]);

        let layer = new Konva.Layer();
        layer.add(line);
        layer.draw();
        ROUTE_DICT[key_name] = {}
        ROUTE_DICT[key_name]["line"] = line
        ROUTE_DICT[key_name]["layer"] = layer
    }
}

function drawStorageRoute() {
    for (var i = 0; i < Object.keys(LINE_DICT).length; i++) {
        if(!Object.keys(ROUTE_DICT).includes(Object.keys(LINE_DICT)[i])) {
            let line = new Konva.Line(LINE_DICT[Object.keys(LINE_DICT)[i]]["line_attr"]);

            let layer = new Konva.Layer();
            layer.add(line);
            layer.draw();
            ROUTE_DICT[Object.keys(LINE_DICT)[i]] = {}
            ROUTE_DICT[Object.keys(LINE_DICT)[i]]["line"] = line
            ROUTE_DICT[Object.keys(LINE_DICT)[i]]["layer"] = layer
        }
    }
}

function loadRoute() {
    // get route from local storage
    var temp
    console.log(getSavedValue("lineDict"));
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

function takeshot(w, h, obj_key) {
    let div = document.getElementById('map');
    let res_dict = {}
    let token = document.head.querySelector("[name~=csrf-token][content]").content;
    
    html2canvas(div, {useCORS: true}).then(
        function (canvas) {
            saveValue("imageData", canvas.toDataURL())
            // document.getElementById('map').remove();
            Sijax.request('famcy_submission_handler', [obj_key, res_dict], { data: { csrf_token: token } });
            // document.getElementById('imgMap').appendChild(canvas);
            // document.getElementById('imgMapHolder').style.display = "block";

            // CANVAS = init_canvas('imgMapMask', w, h)
            // CANVAS_FLAG = true
            // CANVAS_HTML = canvas
            // add_all_route_to_canvas()
        })
}

function add_all_route_to_canvas() {
    if (CANVAS_FLAG) {
        for (var i = 0; i < Object.keys(ROUTE_DICT).length; i++) {
            CANVAS.add(ROUTE_DICT[Object.keys(ROUTE_DICT)[i]]["layer"])
        }
    }
}


function download_img() {
    if (CANVAS_FLAG && CANVAS_HTML) {
        var dt = CANVAS_HTML.toDataURL('image/png');
        document.getElementById('btnDownload').href = dt;
    }
}


function init_canvas(key, w, h) {
    let width = w;
    let height = h;

    let stage = new Konva.Stage({
        id: key+"stage",
        container: key,
        width: width,
        height: height,
    });

    let layer = new Konva.Layer({
        id: key+"trans_layer"
    });
    stage.add(layer);

    let tr = new Konva.Transformer({
        id: key+"trans_trans"
    });
    layer.add(tr);

    // add a new feature, lets add ability to draw selection rectangle
    let selectionRectangle = new Konva.Rect({
        fill: 'rgba(0,0,255,0.5)',
        visible: false,
    });
    layer.add(selectionRectangle);

    let x1, y1, x2, y2, key_name, line;
    stage.on('mousedown touchstart', (e) => {
        // do nothing if we mousedown on any shape
        if (e.target !== stage) {
            return;
        }

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
        for (var i = 0; i < Object.keys(ROUTE_DICT).length; i++) {
            key_name = Object.keys(ROUTE_DICT)[i]
            line = ROUTE_DICT[key_name]["line"]

            // update line dict data
            LINE_DICT[key_name]["line_attr"] = line["attrs"]
        }

        saveValue("lineDict", JSON.stringify(LINE_DICT))
        console.log(getSavedValue("lineDict"))

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
        // if (!e.target.hasName('rect')) {
        //   return;
        // }

        // do we pressed shift or ctrl?
        const metaPressed = e.evt.shiftKey || e.evt.ctrlKey || e.evt.metaKey;
        const isSelected = tr.nodes().indexOf(e.target) >= 0;

        if (!metaPressed && !isSelected) {
          // if no key pressed and the node is not selected
          // select just one
          tr.nodes([e.target]);
        } else if (metaPressed && isSelected) {
          // if we pressed keys and node was selected
          // we need to remove it from selection:
          const nodes = tr.nodes().slice(); // use slice to have new copy of array
          // remove node from array
          nodes.splice(nodes.indexOf(e.target), 1);
          tr.nodes(nodes);
        } else if (metaPressed && !isSelected) {
          // add the node into selection
          const nodes = tr.nodes().concat([e.target]);
          tr.nodes(nodes);
        }
    });


    return stage
}

function loadDb (robot_id, callback) {
    console.log("loadDb")
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

function saveRoute(robot_id) {
    console.log("saveRoute")
    // call API to save data
    if (CANVAS_FLAG && CANVAS_HTML) {
        saveValue("imageData", CANVAS_HTML.toDataURL())
        saveValue("lineDict", JSON.stringify(LINE_DICT))
        const img_data = CANVAS_HTML.toDataURL();
        const line_data = LINE_DICT;

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
}

function clearRoute() {
    LINE_DICT = {}
    saveValue("imageData", "")
    saveValue("lineDict", JSON.stringify(LINE_DICT))
}

