function getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top
    return [x, y]
}

function connect_mousedown_action(_id) {
	const parent = document.getElementById(_id)
	const canvas = parent.getElementsByTagName("canvas")[0]
	const input = parent.getElementsByTagName("input")[0]
	const btn = parent.getElementsByTagName("button")[0]

	canvas.addEventListener('mousedown', function(e) {
	    mousedown_event(e).then(() => {btn.click()});
	})

	async function mousedown_event(e) {
		console.log('mousedown')
	    var pos = getCursorPosition(canvas, e)
	    input.setAttribute("value", "hello")
	}
}
