function generateLineChart(ident, data_list, title) {

  var data = data_list;

  var layout = {
    title: title
  };

  Plotly.newPlot(ident.toString(), data, layout);

}