function generateBarChart(ident, data_list, title, xy_title, size) {

	var data = data_list;

	var layout = {
		width: size[0],
  		height: size[1],
		title: title,
		xaxis: {
			title: xy_title[0],
			tickfont: {
				size: 14,
				color: 'rgb(107, 107, 107)'
			}
		},
		yaxis: {
			title: xy_title[1],
			titlefont: {
				size: 16,
				color: 'rgb(107, 107, 107)'
			},
			tickfont: {
				size: 14,
				color: 'rgb(107, 107, 107)'
			}
		},
		legend: {
			x: 0,
			y: 1.0,
			bgcolor: 'rgba(255, 255, 255, 0)',
			bordercolor: 'rgba(255, 255, 255, 0)'
		},
		barmode: 'group',
		bargap: 0.15,
		bargroupgap: 0.1
	};

	Plotly.newPlot(ident.toString(), data, layout);
}