document.getElementById("header-toggle").addEventListener("click", function() {
	document.getElementById("side-bar").classList.toggle("show");
	document.getElementById("main_win").classList.toggle("open_side_bar");

	for (var i = 0; i < document.getElementsByClassName("toggle_class").length; i++) {
		document.getElementsByClassName("toggle_class")[i].classList.toggle("display_flex")

		if (document.getElementsByClassName("toggle_class")[i].children[1]) {
			document.getElementsByClassName("toggle_class")[i].children[1].classList.toggle("display_block")
		}
	}
});

function btnClickedFunc(e) {
	console.log(e)
	e.nextElementSibling.classList.toggle("display_block");
}