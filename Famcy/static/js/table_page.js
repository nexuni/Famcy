function go_to_page(page_num, _id) {
	var _body = document.getElementById("tbody"+_id);
	var page_body = document.getElementById("switch_page"+_id);

	// set new page size and page num
	if (page_num == "all") {
		page_num = _body.children.length
	}
	page_body.setAttribute("page_size", page_num)
	page_body.children[1].innerHTML = "1"

	// go to first page with new page size
	for (var i = 0; i < _body.children.length; i++) {
		var index = _body.children[i].getAttribute("data-index");
		if (index < page_num) {
			_body.children[i].classList.remove("display_none")
		}
		else {
			_body.children[i].classList.add("display_none")
		}
	}
}

function go_to_next_page(_id) {
	var tbody = document.getElementById("tbody"+_id);
	var page_body = document.getElementById("switch_page"+_id);
	var page_size = parseInt(page_body.getAttribute("page_size"));

	if (page_body.children[1].innerHTML < tbody.children.length / page_size) {
		var new_page = parseInt(page_body.children[1].innerHTML)+1
		page_body.children[1].innerHTML = new_page

		// remove previous page
		for (var i = page_size*(new_page-2); i < page_size*(new_page-1); i++) {
			if (tbody.children.length > i && i >= 0) {
				tbody.children[i].classList.add("display_none")
			}
		}

		// add new page
		for (var i = page_size*(new_page-1); i < page_size*new_page; i++) {
			if (tbody.children.length > i && i >= 0) {
				tbody.children[i].classList.remove("display_none")
			}
		}
	}
}

function go_to_previous_page(_id) {
	var tbody = document.getElementById("tbody"+_id);
	var page_body = document.getElementById("switch_page"+_id);
	var page_size = parseInt(page_body.getAttribute("page_size"));

	if (page_body.children[1].innerHTML > 1) {
		var new_page = parseInt(page_body.children[1].innerHTML)-1
		page_body.children[1].innerHTML = new_page

		// remove previous page
		for (var i = page_size*(new_page+1)-1; i > page_size*new_page-1; i--) {
			if (tbody.children.length > i && i >= 0) {
				tbody.children[i].classList.add("display_none")
			}
		}

		// add new page
		for (var i = page_size*new_page-1; i > page_size*(new_page-1)-1; i--) {
			if (tbody.children.length > i && i >= 0) {
				tbody.children[i].classList.remove("display_none")
			}
		}
	}
	
}

function select_all(e, tbody_id) {
	var _body = document.getElementById(tbody_id);
	var btns = _body.getElementsByClassName("table_btn");

	if (e.checked) {
		for (var i = 0; i < btns.length; i++) {
			btns[i].checked = true
		}
	}
	else {
		for (var i = 0; i < btns.length; i++) {
			btns[i].checked = false
		}
	}
	
}