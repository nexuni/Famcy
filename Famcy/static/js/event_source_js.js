var setInnerHTML = function(elm, html) {
  elm.innerHTML = html;
  Array.from(elm.querySelectorAll("script")).forEach( oldScript => {
    const newScript = document.createElement("script");
    Array.from(oldScript.attributes)
      .forEach( attr => newScript.setAttribute(attr.name, attr.value) );
    newScript.appendChild(document.createTextNode(oldScript.innerHTML));
    oldScript.parentNode.replaceChild(newScript, oldScript);
  });
}

function update_event_source_target(res_dict) {
    console.log("res_dict: ", res_dict)
    if (res_dict["indicator"]) {
        if (typeof res_dict["message"].target_id == "string") {
            if (document.getElementById(res_dict["message"].target_id)) {
                let temp_item = document.getElementById(res_dict["message"].target_id)
                let temp_attr = res_dict["message"].target_attribute

                for (var i = 0; i < Object.keys(temp_attr).length; i++) {
                    temp_item.setAttribute(Object.keys(temp_attr)[i], temp_attr[Object.keys(temp_attr)[i]]);
                }
                setInnerHTML(temp_item, res_dict["message"].target_innerHTML)
            }
        }
        else {
            for (var t = 0; t < res_dict["message"].target_id.length; t++) {
                if (document.getElementById(res_dict["message"].target_id[t])) {
                    let temp_item = document.getElementById(res_dict["message"].target_id[t])
                    let temp_attr = res_dict["message"].target_attribute

                    for (var i = 0; i < Object.keys(temp_attr).length; i++) {
                        temp_item.setAttribute(Object.keys(temp_attr)[i], temp_attr[Object.keys(temp_attr)[i]]);
                    }
                    setInnerHTML(temp_item, res_dict["message"].target_innerHTML[t])
                }
            }
        }
        
    }
}