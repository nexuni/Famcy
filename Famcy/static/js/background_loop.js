// async function background_loop(url, page_id) {
// 	console.log(Sijax.getRequestUri())
// 	Sijax.setRequestUri("/overview")
// 	console.log(Sijax.getRequestUri())
// 	console.log("background_loop!!!!!!!!!!!!!!!!!")
    
//     // Storing response
//     const response = await fetch(url);
//     const res_dict = await response.json();

//     console.log(res_dict)

//     if (res_dict["indicator"]) {
//     	var token = document.head.querySelector("[name~=csrf-token][content]").content
//     	var data = res_dict["message"]

// 		console.log(data, data.page_id)

// 		if (data.page_id  === page_id) {
// 			setTimeout(() => {
// 				Sijax.request('famcy_submission_handler', [data.submission_id, data.data], { data: { csrf_token: token } });
// 			}, 500)
// 		}
//     }
// }

function send_sijax(url, page_id, res) {
	res_dict = JSON.parse(res)
	console.log(res_dict)
	if (res_dict["indicator"]) {
    	var token = document.head.querySelector("[name~=csrf-token][content]").content
    	var data = res_dict["message"]

		if (data.page_id  === page_id) {
			setTimeout(() => {
				Sijax.request('famcy_submission_handler', [data.submission_id, data.data], { data: { csrf_token: token } });
			}, 500)
		}

		return [url, page_id]
    }
}


function background_loop(url, page_id) {
	console.log(url, page_id)

	console.log(Sijax.getRequestUri())
	Sijax.setRequestUri("/overview")
	console.log(Sijax.getRequestUri())
	// fetch(url)
	// 	.then((res) => {
	// 		return res.json();
	// 	})
	// 	.then((res_dict) => {
	// 		console.log(res_dict)
	// 		if (res_dict["indicator"]) {
	// 	    	var token = document.head.querySelector("[name~=csrf-token][content]").content
	// 	    	var data = res_dict["message"]

	// 			if (data.page_id  === page_id) {
	// 				setTimeout(() => {
	// 					Sijax.request('famcy_submission_handler', [data.submission_id, data.data], { data: { csrf_token: token } });
	// 				}, 500)
	// 			}

	// 			return setTimeout(() => background_loop(url, page_id), 5000)
	// 	    }
	// 	})

	// var csrftoken = $('meta[name=csrf-token]').attr('content')

	// $.ajaxSetup({
	//     beforeSend: function(xhr, settings) {
	//         if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
	//             xhr.setRequestHeader("X-CSRFToken", csrftoken)
	//         }
	//     }
	// })

	// var request = $.ajax({
	// 	url: "/bgloop",
	// 	type: "POST",
	// 	contentType: "application/json",
	// 	data: {},  
	// })  
	

	// var defaultRequestParams = {
	// 	"url": Sijax.requestUri,
	// 	"type": "POST",
	// 	"data": {},
	// 	"cache": false,
	// 	"async": true,
	// 	"dataType": "json"
	// };

	// var token = document.head.querySelector("[name~=csrf-token][content]").content
	// requestParams = jQuery.extend(defaultRequestParams, { data: { csrf_token: token } });
	// jQuery.ajax(requestParams).done( function (request) {
	// 	console.log("request: ", request)
	// })

	// if (window.EventSource) {
	// 	var source = new EventSource('/bgloop');
	// 	source.onmessage = function(e) {
	// 		$("#main_win").text(e.data);
	// 	}
	// }

	setInterval(() => {
        fetch(url)
        .then(response => {
                response.text().then(res => {
                	res_dict = JSON.parse(res)
                	console.log(res_dict)
					if (res_dict["indicator"]) {
				    	var token = document.head.querySelector("[name~=csrf-token][content]").content
				    	var data = res_dict["message"]

						if (data.page_id  === page_id) {
							Sijax.request('famcy_submission_handler', [data.submission_id, data.data], { data: { csrf_token: token } });
						}
					}
                })
            })
        .catch(e => {
        	console.log("error: ", e)
        });
        }, 5000);  


	// return new Promise(function(resolve, reject) {

 //        var xmlHttp = new XMLHttpRequest();

 //        xmlHttp.onreadystatechange = function() {
 //            if (xmlHttp.readyState === XMLHttpRequest.DONE) {
 //                if (xmlHttp.status === 200) {
 //                    resolve(send_sijax(url, page_id, xmlHttp.responseText))
 //                }
 //                else {
 //                    reject("Error")
 //                }
 //            }
 //        }

 //        xmlHttp.open("GET", url);
 //        xmlHttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
 //        xmlHttp.send(null);

 //    }).then((res) => {
 //    	console.log(res)
 //    	console.log(process.memoryUsage());
 //    	return setTimeout(() => background_loop(res[0], res[1]), 5000)
 //    })
}

// function awaitHttpGet(url, member_flag){
//     /*
//         Input:
//         - url: (string) the url that you want to send request to
//         - postProcesses: (function) This is the function that should be executed after
//             we got the response from the server `
//     */
    

//     return new Promise(function(resolve, reject) {

//         var xmlHttp = new XMLHttpRequest();

//         xmlHttp.onreadystatechange = function() {
//             if (xmlHttp.readyState === XMLHttpRequest.DONE) {
//                 if (xmlHttp.status === 200) {
//                     resolve(xmlHttp.responseText)
//                 }
//                 else {
//                     reject("Error")
//                 }
//             }
//         }

//         xmlHttp.open("GET", url);

//         // if (member_flag) {
//         var key = process.env.REACT_APP_GADGET_KEY
//         var secret = process.env.REACT_APP_SECRET
//         var time_shift = 8
//         xmlHttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
//         xmlHttp.setRequestHeader("Gadgethi-Key", key.toString())
//         xmlHttp.setRequestHeader("Hmac256-Result", HMAC256_encryption(key, secret, time_shift).toString())
//         xmlHttp.setRequestHeader("time", (time_standard(time_shift)).toString())
//         // }

//         xmlHttp.send(null);

//     })
// }