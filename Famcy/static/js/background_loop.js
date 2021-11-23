async function background_loop(url, page_id) {
	console.log("background_loop!!!!!!!!!!!!!!!!!")
    
    // Storing response
    const response = await fetch(url);
    const res_dict = await response.json();

    console.log(res_dict)

    if (res_dict["indicator"]) {
    	var token = document.head.querySelector("[name~=csrf-token][content]").content
    	var data = res_dict["message"]

		console.log(data, data.page_id)
		
		if (data.page_id  === page_id) {
			Sijax.request('famcy_submission_handler', [data.submission_id, data.data], { data: { csrf_token: token } });
		}
    }
    
    // Storing data in form of JSON
    // var data = await response.json();
    
    // if (response) {
        // hideloader
    // }
}