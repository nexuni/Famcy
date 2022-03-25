function go_to_page(page_num, tbody_id) {
	var _body = document.getElementById(tbody_id);
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