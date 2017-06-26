var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var svg = d3.select("div.col1").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var chart_data;

function buildChart( data ) {

  chart_data = data;

  data.forEach(function(d) {
      d.Name = d.Name;
      d.Val = +d.Val;
  });

  var t = d3.transition()
    .delay(500)
    .duration(2500)

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

  var max_x = d3.max(data, function(d) { return +d.Val;} );

  var bars = svg.selectAll(".bar")
    .data( data );

  bars.enter().append("rect")
    .attr("class","bar")
    .attr("x", function(d) { return ( d.Val > 0)?( x(Math.min(0, d.Val) + 0.1*max_x) ):( x(Math.min(0, d.Val) - 0.1*max_x) ); })
    .attr("fill", function(d){ return ( d.Val > 0)?( "red" ):( "green" ); })
    .transition()
    .duration(1000)
    .ease( 'bounce' )
    .attr("class", "bar")
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

function colorChart( pos_color, neg_color ) {

  svg.selectAll(".bar")
    .attr("fill", function(d){ return ( d.Val > 0)?( pos_color ):( neg_color ); })

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
    .data( data );

  // EXIT old elements not present in new data.
  bars.exit()
    .attr("class", "bar")
    .transition()
    .duration(300)
    .ease("exp")
    .attr("width", 0)
    .remove();

  // UPDATE old elements present in new data.s
  bars
    .attr("class","bar")
    .transition(t)
    .attr("x", function(d) { return x(Math.min(0, d.Val)); })
    .attr("y", function(d) { return y(d.Name); })
    .attr("width", function(d) { return Math.abs(x(d.Val) - x(0)); })
    .attr("height", y.rangeBand())
    .attr("fill", function(d){ return ( d.Val > 0)?( "red" ):( "green" ); });

  var max_x = d3.max(data, function(d) { return +d.Val;} );

  // ENTER new elements present in new data.
  bars.enter().append("rect")
    .attr("class","bar")
    .attr("x", function(d) { return ( d.Val > 0)?( x(Math.min(0, d.Val) + 0.1*max_x) ):( x(Math.min(0, d.Val) - 0.1*max_x) ); })
    .attr("fill", function(d){ return ( d.Val > 0)?( "red" ):( "green" ); })
    .transition()
    .duration(1000)
    .ease( 'bounce' )
    .attr("y", function(d) { return y(d.Name); })
    .attr("x", function(d) { return x(Math.min(0, d.Val)); })
    .attr("width", function(d) { return Math.abs(x(d.Val) - x(0)); })
    .attr("fill", function(d){ return ( d.Val > 0)?( "red" ):( "green" ); })
    .attr("height", y.rangeBand());

  svg.selectAll(".y.axis")
    .transition(t)
    .attr("transform", "translate(" + x(0) + ",0)")
    .call(yAxis);

  svg.selectAll(".x.axis")
    .transition(t)
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

    chart_data = data;

}

d3.select("input").on("change", change);

function change() {

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

  var c = document.getElementById('box-sort');

  // Copy-on-write since tweens are evaluated after a delay.
  var x0 = y.domain( chart_data.sort( c.checked
      ? function(a, b) { return b.Val - a.Val; }
      : function(a, b) { return d3.ascending(a.Name, b.Name); })
      .map(function(d) { return d.Name; }))
      .copy();

  svg.selectAll(".bar")
      .sort(function(a, b) { return x0(a.Name) - x0(b.Name); });

  var transition = svg.transition().duration(750),
      delay = function(d, i) { return i * 50; };

  transition.selectAll(".bar")
      .delay(delay)
      .attr("y", function(d) { return x0(d.Name); });

  transition.select(".y.axis")
      .call(yAxis)
    .selectAll("g")
      .delay(delay);

}
