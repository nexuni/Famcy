

function generatePieChart(ident, values, labels, size) {
	var data = [{
	  type: "pie",
	  values: values,
	  labels: labels,
	  textinfo: "label+percent",
	  insidetextorientation: "radial"
	}]

	var layout = [{
	  height: size[1],
	  width: size[0]
	}]

	Plotly.newPlot(ident.toString(), data, layout)
}


