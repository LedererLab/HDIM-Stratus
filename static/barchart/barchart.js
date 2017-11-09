class BarChart {

  constructor( divName ) {

    this.tip_ = d3.tip()
      .attr('class', 'd3-tip')
      .offset([-10, 0])
      .html(function(d) {
          return "<strong>" + d.Name + ":</strong> <span style='color: #D3D3D3'>" + d.Val + "</span>";

      })

    var margin_ = {top: 20, right: 20, bottom: 30, left: 40};

    var this_ = this;

    this_.divName_ = divName;

    this_.posColor_ = '#811d5e';
    this_.negColor_ = '#fed800';

    this_.sortValues_ = true;

    this_.chartData_ = {};

    this_.width_ = 920 - margin_.left - margin_.right;
    this_.height_ = 720 - margin_.top - margin_.bottom;

    this_.svg_ = d3.select("div." + divName ).append("svg")
        .attr("width", this_.width_ + margin_.left + margin_.right)
        .attr("height", this_.height_ + margin_.top + margin_.bottom)
        .attr("class", "graph-svg-component")
        .append("g")
        .attr("transform", "translate(" + margin_.left + "," + margin_.top + ")");

    var x = d3.scale.linear()
        .range([0, this_.width_]);

    var y = d3.scale.ordinal()
        .rangeRoundBands([0, this_.height_], 0.1);

    this_.xAxis_ = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    this_.yAxis_ = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickSize(0)
        .tickPadding(6);

    function make_x_axis() {
        return d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(5)
    }

      // Draw the x Grid lines
    this_.svg_.append("g")
      .attr("class", "grid")
      .attr("transform", "translate(0," + this_.height_ + ")")
      .call(make_x_axis()
          .tickSize( - this_.height_, 0, 0)
          .tickFormat("")
      )

    this_.svg_.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + this_.height_ + ")")
      .call(this_.xAxis_);

    this_.svg_.append("g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + x(0) + ",0)")
      .call(this_.yAxis_);

  }

  setPosColor( posColor ) {

    var this_ = this;

    this_.posColor_ = d3.rgb( posColor );
    this.colorVals_();

  }

  setNegColor( negColor ) {

    var this_ = this;

    this_.negColor_ = d3.rgb( negColor );
    this.colorVals_();

  }

  colorVals_() {

    var this_ = this;

    this_.svg_.selectAll(".bar")
      .transition()
      .duration(1000)
      .attr("fill", function(d){ return ( d.Val > 0)?( this_.posColor_ ):( this_.negColor_ ); })

  }

  makeXAxis_() {
    return d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks(5)
  }

  coerceData_( data ) {
    data.forEach(function(d) {
        d.Name = d.Name;
        d.Val = +d.Val;
    });
  }

  updateChart( data ) {

    var this_ = this;

    this_.chartData_ = data;
    this_.sortValues = true;

    this_.coerceData_( data );

    var x = d3.scale.linear()
        .range([0, this_.width_]);

    var y = d3.scale.ordinal()
        .rangeRoundBands([0, this_.height_], 0.1);

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

      // function for the x grid lines
    function make_x_axis() {
        return d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(5)
    }

    var t = d3.transition()
        .duration(750)

    // Draw the x Grid lines
    this_.svg_.selectAll(".grid")
    .transition(t)
    .attr("transform", "translate(0," + this_.height_ + ")")
    .call(make_x_axis()
        .tickSize(-this_.height_, 0, 0)
        .tickFormat("")
    )

    // JOIN new data with old elements.
    var bars = this_.svg_.selectAll(".bar")
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
      .attr("fill", function(d){ return ( d.Val > 0)?( this_.posColor_ ):( this_.negColor_ ); })
      .transition(t)
      .duration(1000)
      .ease( 'bounce' )
      .attr("x", function(d) { return x(Math.min(0, d.Val)); })
      .attr("y", function(d) { return y(d.Name); })
      .attr("width", function(d) { return Math.abs(x(d.Val) - x(0)); })
      .attr("height", y.rangeBand())
      .attr("fill", function(d){ return ( d.Val > 0)?( this_.posColor_ ):( this_.negColor_ ); });

    var max_x = d3.max(data, function(d) { return +d.Val;} );

    // ENTER new elements present in new data.
    bars.enter().append("rect")
      .attr("class","bar")
      .attr("fill", function(d){ return ( d.Val > 0)?( this_.posColor_ ):( this_.negColor_ ); })
      .transition()
      .duration(1000)
      .ease( 'bounce' )
      .attr("y", function(d) { return y(d.Name); })
      .attr("x", function(d) { return x(Math.min(0, d.Val)); })
      .attr("width", function(d) { return Math.abs(x(d.Val) - x(0)); })
      .attr("fill", function(d){ return ( d.Val > 0)?( this_.posColor_ ):( this_.negColor_ ); })
      .attr("height", y.rangeBand());

    this_.svg_.call( this_.tip_ );

    bars
      .on('mouseover', this_.tip_.show)
      .on('mouseout', this_.tip_.hide);

    bars.on( "click", () => this.sortBars() );

    this_.svg_.selectAll(".y.axis")
      .transition(t)
      .attr("transform", "translate(" + x(0) + ",0)")
      .call(yAxis);

    this_.svg_.selectAll(".x.axis")
      .transition(t)
      .attr("transform", "translate(0," + this_.height_ + ")")
      .call(xAxis);

  }

  sortBars() {

    var this_ = this;

    var x = d3.scale.linear()
        .range([0, this_.width_]);

    var y = d3.scale.ordinal()
        .rangeRoundBands([0, this_.height_], 0.1);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .tickSize(0)
        .tickPadding(6);

    // Copy-on-write since tweens are evaluated after a delay.
    var x0 = y.domain( this_.chartData_.sort( this_.sortValues
        ? function(a, b) { return b.Val - a.Val; }
        : function(a, b) { return d3.ascending(a.Name, b.Name); })
        .map(function(d) { return d.Name; }))
        .copy();

    this_.svg_.selectAll(".bar")
        .sort(function(a, b) { return x0(a.Name) - x0(b.Name); });

    var transition = this_.svg_.transition().duration(750),
        delay = function(d, i) { return i * 50; };

    transition.selectAll(".bar")
        .delay(delay)
        .attr("y", function(d) { return x0(d.Name); });

    transition.select(".y.axis")
        .call(yAxis)
        .selectAll("g")
        .delay(delay);

        this_.sortValues =! this_.sortValues;

  }

  digestData_( raw_data ) {

    return raw_data.map( function(e) { return e.Name + "," + e.Val + "\n"; } )
      .join("")
      .slice(0, - 1); // remove last line break

  }

  downloadText_ ( filename, text ) {
    var pom = document.createElement('a');
    pom.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    pom.setAttribute('download', filename);

    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
  }

  dumpData() {

    var this_ = this;

    var bar_data = this_.svg_.selectAll(".bar")
      .data();

    var csv_data = this.digestData_( bar_data );

    this.downloadText_( "Regression_Result.csv", csv_data );
  }

  dumpImage() {

      var this_ = this;

      /*
      Based off  gustavohenke's svg2png.js
      gist.github.com/gustavohenke/9073132
      */

      // var svg = document.querySelector( "svg" );

      var svg = d3.select('svg').node();

      // var svg = this_.svg_.node();

      var svgData = new XMLSerializer().serializeToString( svg );

      var canvas = document.createElement( "canvas" );

      var rect_ = d3.select("div." + this_.divName_ ).node().getBoundingClientRect();

      canvas.width = rect_.width;
      canvas.height = rect_.height;

      var ctx = canvas.getContext( "2d" );

      var dataUri = '';
      try {
          dataUri = 'data:image/svg+xml;base64,' + btoa(svgData);
      } catch (ex) {

          // For browsers that don't have a btoa() method, send the text off to a webservice for encoding
          // Uncomment if needed (requires jQuery)
          $.ajax({
              url: "http://www.mysite.com/webservice/encodeString",
              data: { svg: svgData },
              type: "POST",
              async: false,
              success: function(encodedSVG) {
                  dataUri = 'data:image/svg+xml;base64,' + encodedSVG;
              }
          })

      }

      var img = document.createElement( "img" );

      img.onload = function() {
          ctx.drawImage( img, 0, 0 );

          try {

              // Try to initiate a download of the image
              var a = document.createElement("a");
              a.download = "Regression_Results.png";
              a.href = canvas.toDataURL("image/png");
              document.querySelector("body").appendChild(a);
              a.click();
              document.querySelector("body").removeChild(a);

          } catch (ex) {

              // If downloading not possible (as in IE due to canvas.toDataURL() security issue)
              // then display image for saving via right-click

              var imgPreview = document.createElement("div");
              imgPreview.appendChild(img);
              document.querySelector("body").appendChild(imgPreview);

          }
      };

      img.src = dataUri;
      console.log( img );

    }

}
