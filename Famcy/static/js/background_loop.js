function background_loop(url, route, time=5000) {

	Sijax.setRequestUri(route)
	
    fetch(url)
        .then(response => {
    		return response.json()
        })
        .then(res_dict => {
        	
        	if (res_dict["indicator"]) {
        		if (document.getElementById(res_dict["message"].target_id)) {
        			let temp_item = document.getElementById(res_dict["message"].target_id)
        			let temp_attr = res_dict["message"].target_attribute

        			for (var i = 0; i < Object.keys(temp_attr).length; i++) {
        				temp_item.setAttribute(Object.keys(temp_attr)[i], temp_attr[Object.keys(temp_attr)[i]]);
        			}
        			
        			temp_item.innerHTML = res_dict["message"].target_innerHTML
        		}
            }

            setTimeout(() => {background_loop(url, route)}, time);
        	
        })
        .catch(e => {
        	console.log("error: ", e)
        });
}