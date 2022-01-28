var purePgmData, rect;

function displayContents(contents, c_id) {
    var canvas = document.getElementById(c_id);
    var ctx = canvas.getContext('2d');

    function putImageData(ctx, data) {
        for (var y = 0; y < canvas.height; y++) {
            for (var x = 0; x < canvas.width; x++) {
                ctx.fillStyle = 'rgba(' + data[y][x]
                                + ',' + data[y][x]
                                + ',' + data[y][x]
                                + ', 1)';
                ctx.fillRect(x, y, 1, 1);

            }
        }

        purePgmData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    }

    putImageData(ctx, contents);
}

function displayRoute(contents, c_id, r, origin, w, h, color) {
    var canvas = document.getElementById(c_id);
    var ctx = canvas.getContext('2d');

    function displayRobotRoute(ctx, data, _r, _x, _y, _w, _h, _color) {
        var x, y;
        var rightp = _w*_r + _x;
        var leftp = _x;
        var topp = _h*_r + _y;
        var lowp = _y;
        var p = 1/_r;

        for (var i = 0; i < data.length; i++) {
            ctx.fillStyle = _color;
            x = (data[i]["x"]-leftp)*p;
            y = (topp-data[i]["y"])*p;
            ctx.fillRect(x-4, y-4, 8, 8);
        }
    }

    displayRobotRoute(ctx, contents, r, origin[0], origin[1], w, h, color);
}

function dragElement(e, c_id) {
    var elmnt = document.getElementById(c_id)

    if (elmnt.getAttribute("drag_flag") == "true") {
        e.classList.remove("pgm_btn_pressed")
        elmnt.setAttribute("drag_flag", "false")
        elmnt.onmousedown = null
    }
    else {
        if (document.getElementsByClassName("pgm_btn_pressed").length >= 1) {
            document.getElementsByClassName("pgm_btn_pressed")[0].classList.remove("pgm_btn_pressed")
        }
        e.classList.add("pgm_btn_pressed")
        elmnt.setAttribute("drag_flag", "true")
        elmnt.setAttribute("draw_flag", "false")
        elmnt.setAttribute("click_flag", "false")
        var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        elmnt.onmousedown = dragMouseDown
    }
    

    function dragMouseDown(e) {
        console.log("dragMouseDown")
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        console.log("elementDrag")
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        console.log("closeDragElement")
        /* stop moving when mouse button is released:*/
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

function resetElement(c_id) {
    var elmnt = document.getElementById(c_id)
    var ctx = elmnt.getContext('2d');
    elmnt.style.top = "0px";
    elmnt.style.left = "0px";

    elmnt.style.transform = "scale(1)";
    elmnt.setAttribute("scale_rate", 1);

    ctx.putImageData(purePgmData, 0, 0);

    if (document.getElementsByClassName("pgm_btn_pressed").length >= 1) {
        document.getElementsByClassName("pgm_btn_pressed")[0].classList.remove("pgm_btn_pressed")
    }
    elmnt.setAttribute("drag_flag", "false")
    elmnt.setAttribute("draw_flag", "false")
    elmnt.setAttribute("click_flag", "false")

    elmnt.onmousedown = null
}

function scaleElement(c_id, s_rate) {
    var elmnt = document.getElementById(c_id);
    var scale_rate = elmnt.getAttribute("scale_rate");

    scale_rate *= s_rate;
    elmnt.style.transform = "scale("+scale_rate+")";
    elmnt.setAttribute("scale_rate", scale_rate);

    if (document.getElementsByClassName("pgm_btn_pressed").length >= 1) {
        document.getElementsByClassName("pgm_btn_pressed")[0].classList.remove("pgm_btn_pressed")
    }
    elmnt.setAttribute("drag_flag", "false")
    elmnt.setAttribute("draw_flag", "false")
    elmnt.setAttribute("click_flag", "false")

    elmnt.onmousedown = null

}

function drawArrowOnElement(e, c_id, color="#000000") {
    var elmnt = document.getElementById(c_id)
    var ctx = elmnt.getContext('2d');
    var rect = elmnt.getBoundingClientRect();
    var scale = elmnt.getBoundingClientRect().width / elmnt.offsetWidth;

    if (elmnt.getAttribute("draw_flag") == "true") {
        e.classList.remove("pgm_btn_pressed")
        elmnt.setAttribute("draw_flag", "false")
        elmnt.onmousedown = null
    }
    else {
        if (document.getElementsByClassName("pgm_btn_pressed").length >= 1) {
            document.getElementsByClassName("pgm_btn_pressed")[0].classList.remove("pgm_btn_pressed")
        }
        e.classList.add("pgm_btn_pressed")
        elmnt.setAttribute("draw_flag", "true")
        elmnt.setAttribute("drag_flag", "false")
        elmnt.setAttribute("click_flag", "false")
        var originx = 0, originy = 0, posx = 0, posy = 0;
        elmnt.onmousedown = drawMouseDown
    }
    

    function drawMouseDown(e) {
        console.log("drawMouseDown")
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        originx = (e.clientX-rect.left)/scale;
        originy = (e.clientY-rect.top)/scale;
        posx = (e.clientX-rect.left)/scale;
        posy = (e.clientY-rect.top)/scale;
        ctx.beginPath();
        ctx.moveTo(posx,posy);
        document.onmouseup = closeDrawElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDraw;
    }

    function elementDraw(e) {
        console.log("elementDraw")
        e = e || window.event;
        e.preventDefault();
        posx = (e.clientX-rect.left)/scale;
        posy = (e.clientY-rect.top)/scale;
        // calculate the new cursor position:
        // ctx.lineTo(e.clientX-rect.left,e.clientY-rect.top);
    }

    function closeDrawElement() {
        console.log("closeDrawElement")
        angle = (-1) * Math.atan((posy-originy) / (posx-originx))*180/Math.PI;
        arrow_size = 10

        ctx.lineTo(posx,posy);
        ctx.closePath();
        ctx.strokeStyle = color;
        ctx.stroke();

        drawLineWithArrows(originx,originy,posx,posy,10,10,false,true)

        ctx.beginPath();
        ctx.moveTo(originx,originy);
        if (originx>posx) {
            ctx.lineTo(originx-10,originy);
        }
        else{
            ctx.lineTo(originx+10,originy);
        }
        
        ctx.closePath();
        ctx.strokeStyle = color;
        ctx.stroke();

        ctx.beginPath();
        ctx.font = "15px Arial";
        if (posx<originx) {
            originx -= 80
            if (posy<originy) {
                // 3
                angle += 180
            }
            else {
                // 2
                angle += 180
            }
        }
        else {
            originx += 30
            if (posy<originy) {
                // 1
                angle += 0
            }
            else {
                // 4
                angle += 360
            }
        }
        ctx.fillStyle = color;
        ctx.fillText(Math.round(angle * 100)/100+"º", originx, originy);
        ctx.closePath();
        
        /* stop moving when mouse button is released:*/
        document.onmouseup = null;
        document.onmousemove = null;
    }

    function drawLineWithArrows(x0,y0,x1,y1,aWidth,aLength,arrowStart,arrowEnd){
        var dx=x1-x0;
        var dy=y1-y0;
        var angle=Math.atan2(dy,dx);
        var length=Math.sqrt(dx*dx+dy*dy);
        ctx.translate(x0,y0);
        ctx.rotate(angle);
        ctx.beginPath();
        ctx.moveTo(0,0);
        ctx.lineTo(length,0);
        if(arrowStart){
            ctx.moveTo(aLength,-aWidth);
            ctx.lineTo(0,0);
            ctx.lineTo(aLength,aWidth);
        }
        if(arrowEnd){
            ctx.moveTo(length-aLength,-aWidth);
            ctx.lineTo(length,0);
            ctx.lineTo(length-aLength,aWidth);
        }
        ctx.stroke();
        ctx.setTransform(1,0,0,1,0,0);
    }
}

function getPointXYValue(e, c_id, x, y, r, color="#000000") {
    var elmnt = document.getElementById(c_id)
    var ctx = elmnt.getContext('2d');
    var rect = elmnt.getBoundingClientRect();
    var scale = elmnt.getBoundingClientRect().width / elmnt.offsetWidth;

    if (elmnt.getAttribute("click_flag") == "true") {
        e.classList.remove("pgm_btn_pressed")
        elmnt.setAttribute("click_flag", "false")
        elmnt.onmousedown = null
    }
    else {
        if (document.getElementsByClassName("pgm_btn_pressed").length >= 1) {
            document.getElementsByClassName("pgm_btn_pressed")[0].classList.remove("pgm_btn_pressed")
        }
        e.classList.add("pgm_btn_pressed")
        elmnt.setAttribute("click_flag", "true")
        elmnt.setAttribute("drag_flag", "false")
        elmnt.setAttribute("draw_flag", "false")
        var originx, originy;
        elmnt.onmousedown = clickMouseDown
    }
    

    function clickMouseDown(e) {
        console.log("clickMouseDown")
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        originx = (e.clientX-rect.left)/scale;
        originy = (e.clientY-rect.top)/scale;
        document.onmouseup = closeDragElement;
    }

    function closeDragElement() {
        console.log("closeDragElement")
        /* stop moving when mouse button is released:*/

        ctx.beginPath();
        ctx.font = "15px Arial";
        ctx.fillStyle = color;

        ctx.fillRect(originx-4, originy-4, 8, 8);

        var new_p = tramsform_xy_value(originx, originy)

        if (originx > elmnt.width / 2) {
            ctx.fillText("x: "+new_p[0]+" y: "+new_p[1], originx-120, originy);
        }

        else {
            ctx.fillText("x: "+new_p[0]+" y: "+new_p[1], originx+8, originy);
        }

        ctx.closePath();

        document.onmouseup = null;
        document.onmousemove = null;
    }

    function tramsform_xy_value(p_x, p_y) {
        return [Math.round((p_x * r + x) * 100)/100, Math.round((p_y * r + y) * 100)/100]
    }
}











// function setToolBar(e) {
//     // Canvas
//     var mouseDown = false;
//     var mousePos = [0, 0];
//     var canvas = document.querySelector("#myCanvas");
//     var context = canvas.getContext("2d");
//     // canvas.addEventListener("mousewheel", zoom, false);
//     canvas.addEventListener("mousedown", setMouseDown, false);
//     canvas.addEventListener("mouseup", setMouseUp, false);
//     canvas.addEventListener("mousemove", move, false);

//     // Defaults
//     var DEFAULT_ZOOM = .5;
//     var MAX_ZOOM = 3;
//     var MIN_ZOOM = .2;
//     var ZOOM_STEP = .1;
//     // var DRAW_POS = [0, 0];
//     var DRAW_POS = [canvas.width/2, canvas.height/2];

//     // Buttons
//     var zoomInBtn = document.querySelector("#zoomIn");
//     zoomInBtn.addEventListener("click", zoomIn, false);
//     var zoomOutBtn = document.querySelector("#zoomOut");
//     zoomOutBtn.addEventListener("click", zoomOut, false);
//     var resetZoomBtn = document.querySelector("#resetZoom");
//     resetZoomBtn.addEventListener("click", resetZoom, false);
//     var resetPosBtn = document.querySelector("#resetPos");
//     resetPosBtn.addEventListener("click", resetPos, false);

//     // Image
//     var loaded = false;
//     var drawPos = DRAW_POS;
//     var scale = DEFAULT_ZOOM;
//     var image = new Image();
//     image.src = "./test.jpg";
//     image.addEventListener("load", function(e) {
//         loaded = true;
//         drawCanvas();
//     }, false);

//     // Draw the canvas
//     function drawCanvas() {
//         context.fillStyle = "#FFFFFF";
//         context.fillRect(0,0,canvas.width,canvas.height);
//         if (loaded) {
//             drawImage();
//         }
//     }

//     // Draw the image
//     function drawImage() {
//         var w = image.width * scale;
//         var h = image.height * scale;
//         // var x = drawPos[0];
//         // var y = drawPos[1]; 
//         var x = drawPos[0] - (w / 2);
//         var y = drawPos[1] - (h / 2);
//         context.drawImage(image, x, y, w, h);
//     }
    
//     // Set the zoom with the mouse wheel
//     function zoom(e) {
//         if (e.wheelDelta > 0) {
//             zoomIn();
//         }
//         else {
//             zoomOut();
//         }
//     }

//     // Zoom in
//     function zoomIn(e) {
//         if (scale < MAX_ZOOM) {
//             scale += ZOOM_STEP;
//             drawCanvas();
//         }
//     }

//     // Zoom out
//     function zoomOut(e) {
//         if (scale > MIN_ZOOM) {
//             scale -= ZOOM_STEP;
//             drawCanvas();
//         }
//     }

//     // Reset the zoom
//     function resetZoom(e) {
//         scale = DEFAULT_ZOOM;
//         drawCanvas();
//     }

//     // Reset the position
//     function resetPos(e) {
//         drawPos = DRAW_POS;
//         drawCanvas();
//     }

//     // Toggle mouse status
//     function setMouseDown(e) {
//         mouseDown = true;
//         mousePos = [e.x, e.y];
//     }
//     function setMouseUp(e) {
//         mouseDown = false;
//     }

//     // Move
//     function move(e) {
//         if (mouseDown) {
//             var dX = 0, dY = 0;
//             var delta = [e.x - mousePos[0], e.y - mousePos[1]];
//             drawPos = [drawPos[0] + delta[0], drawPos[1] + delta[1]];
//             mousePos = [e.x, e.y];
//             drawCanvas();
//         }
//     }
// }


// document.addEventListener("DOMContentLoaded", (e) => setToolBar(e), true);
