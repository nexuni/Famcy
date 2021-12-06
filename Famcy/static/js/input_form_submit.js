function input_form_main_btn_submit(e, loader_flag, form_id, form_obj_key, btn_obj_key) {

	if (loader_flag) {
		$('#loading_holder').css("display","flex");
	}

	var form_element = document.getElementById(form_id)
	var formData = new FormData(form_element)
	var response_dict = {}
	for (var pair of formData.entries()) {
		if (pair[0] !== "btSelectAll") {
			if (!(pair[0] in response_dict)) {
				response_dict[pair[0]] = [pair[1]]
			}
			else {
				response_dict[pair[0]].push(pair[1])
			}
		}
	}

	var flag = checkform(form_element, form_obj_key)
	var token = document.head.querySelector("[name~=csrf-token][content]").content
	if (flag) {
		Sijax.request('famcy_submission_handler', [btn_obj_key, response_dict], { data: { csrf_token: token } });
	}
};