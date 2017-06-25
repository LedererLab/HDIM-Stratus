var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var svg = d3.select("div.col1").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


function buildChart( data ) {

  data.forEach(function(d) {
      d.Name = d.Name;
      d.Val = +d.Val;
  });

  var x = d3.scale.linear()
      .range([0, width]);

  var y = d3.scale.ordinal()
      .rangeRoundBands([0, height], 0.1);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .tickSize(0)
      .tickPadding(6);

  x.domain(d3.extent(data, function(d) { return d.Val; })).nice();
  y.domain(data.map(function(d) { return d.Name; }));

  svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .attr("class", function(d) { return "bar bar--" + (d.Val < 0 ? "negative" : "positive"); })
    .attr("x", function(d) { return x(Math.min(0, d.Val)); })
    .attr("y", function(d) { return y(d.Name); })
    .attr("width", function(d) { return Math.abs(x(d.Val) - x(0)); })
    .attr("height", y.rangeBand());

  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

  svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(" + x(0) + ",0)")
    .call(yAxis);

}

function updateChart( data ) {

  data.forEach(function(d) {
      d.Name = d.Name;
      d.Val = +d.Val;
  });

  var x = d3.scale.linear()
      .range([0, width]);

  var y = d3.scale.ordinal()
      .rangeRoundBands([0, height], 0.1);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .tickSize(0)
      .tickPadding(6);

  x.domain(d3.extent(data, function(d) { return d.Val; })).nice();
  y.domain(data.map(function(d) { return d.Name; }));

  var t = d3.transition()
      .duration(750)

  // JOIN new data with old elements.
  var bars = svg.selectAll(".bar")
    .data(data, function(d) { return d; });

  // UPDATE old elements present in new data.
  bars.attr("class", "update")
    .transition(t)
    .attr("x", function(d) { return x(Math.min(0, d.Val)); })
    .attr("y", function(d) { return y(d.Name); })
    .attr("width", function(d) { return Math.abs(x(d.Val) - x(0)); })
    .attr("height", y.rangeBand());

  // EXIT old elements not present in new data.
  bars.exit()
      .attr("class", "exit")
      .remove();

  // ENTER new elements present in new data.
  svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .transition(t)
    .attr("class", function(d) { return "bar bar--" + (d.Val < 0 ? "negative" : "positive"); })
    .attr("x", function(d) { return x(Math.min(0, d.Val)); })
    .attr("y", function(d) { return y(d.Name); })
    .attr("width", function(d) { return Math.abs(x(d.Val) - x(0)); })
    .attr("height", y.rangeBand());

  svg.selectAll(".y.axis")
    .transition(t)
    .attr("transform", "translate(" + x(0) + ",0)")
    .call(yAxis);

  svg.selectAll(".x.axis")
    .transition(t)
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

}

// function update(data) {
//   var t = d3.transition()
//       .duration(750);
//
//   // JOIN new data with old elements.
//   var text = g.selectAll("text")
//     .data(data, function(d) { return d; });
//
//   // EXIT old elements not present in new data.
//   text.exit()
//       .attr("class", "exit")
//     .transition(t)
//       .attr("y", 60)
//       .style("fill-opacity", 1e-6)
//       .remove();
//
//   // UPDATE old elements present in new data.
//   text.attr("class", "update")
//       .attr("y", 0)
//       .style("fill-opacity", 1)
//     .transition(t)
//       .attr("x", function(d, i) { return i * 32; });
//
//   // ENTER new elements present in new data.
//   text.enter().append("text")
//       .attr("class", "enter")
//       .attr("dy", ".35em")
//       .attr("y", -60)
//       .attr("x", function(d, i) { return i * 32; })
//       .style("fill-opacity", 1e-6)
//       .text(function(d) { return d; })
//     .transition(t)
//       .attr("y", 0)
//       .style("fill-opacity", 1);
// }
