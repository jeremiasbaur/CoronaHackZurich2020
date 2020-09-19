/**
 * Code inspired by: https://schuelerzahlen-zuerich.opendata.iwi.unibe.ch/App2/d3geo-2/ch_var/map.js
 */

// hide the form if the browser doesn't do SVG,
// (then just let everything else fail)
if (!document.createElementNS) {
  document.getElementsByTagName("form")[0].style.display = "none";
}

// Define the colors with colorbrewer
var colors = colorbrewer.RdYlBu[3]
    .reverse()
    .map(function(rgb) { return d3.hsl(rgb); });

// Set the (initial) width and height of the map
var width = 960,
    height = 600;

// Define the elements needed for map creation
var body = d3.select("body"),
    map = d3.select("#map").attr("preserveAspectRatio", "xMidYMid")
        .attr("viewBox", "0 0 " + width + " " + height),
    layer = map.append("g")
        .attr("id", "layer"),
    mapFeatures = layer.append("g")
        .attr("id", "mapFeatures")
        .selectAll("path"),
    tooltip = d3.select("#map-container")
        .append("div")
        .attr("class", "ttip hidden");

// Define the projection of the map (center and scale will be defined
// later)
var proj = d3.geo.mercator();

// Prepare the cartogram
var topology,
    geometries,
    dataById = {},
    carto = d3.cartogram()
        .projection(proj);

// Define the fields of the data
var fields = [
      {name: "(no scale)", id: "none"},
      {name: "Number of tweets", id: "tweets_total", key: "%d"}
    ],
    day = 10;

// D3's "change" event is somehow not triggered when selecting the
// dropdown value programmatically. Use jQuery's change event instead.
$('#day').on("change", function(e) {
  // On change, update the URL hash
  day = parseInt(this.value);
  console.log(day);
  update();
});

d3.select("#keywords")
  .on("change", function(e) {
  // On change, update the URL hash
  keywords = this.value;
  update();
});

// Read the geometry data
d3.json("static/ch_cantons.topojson", function(topo) {
  topology = topo;

  // The mapped unit for cantons: Cantons
  geometries = topology.objects.cantons.geometries;

  init();
});


/**
 * Initialize the map. Creates the basic map without scaling of the
 * features.
 */
function init() {

  // Create the cartogram features (without any scaling)
  var features = carto.features(topology, geometries),
      path = d3.geo.path()
          .projection(proj);

  // Determine extent of the topology
  var b = topology.bbox;
  t = [(b[0]+b[2])/2, (b[1]+b[3])/2];
  s = 0.95 / Math.max(
      (b[2] - b[0]) / width,
      (b[3] - b[1]) / height
  );

  // Scale it to fit nicely
  s = s * 55;
  proj
      .scale(s)
      .center(t).translate([width / 2, height / 2]);

  // Put the features on the map
  mapFeatures = mapFeatures.data(features)
      .enter()
      .append("path")
      .attr("class", "mapFeature")
      .attr("id", function(d) {
        return getName(d);
      })
      .attr("fill", "#fafafa")
      .attr("d", path);
}

update();
keywords = "";
function update() {
  // load and display Tweets
  d3.json("static/cleaned_tweets_en.json", function(t1) {
    var tweets = []
    tweets.push(...t1);
    d3.json("static/cleaned_tweets_de.json", function(t2) {
      tweets.push(...t2);
      tweets = tweets.filter(tweet => new Date(tweet.date).getDate() === day);
      console.log(tweets)

      if (keywords !== "") {
        tweets = tweets.filter(tweet => keywords.split(',').some(keyword => tweet.text.toLowerCase().indexOf(keyword.toLowerCase()) !== -1));
      }

      function computeSentimentColor(sentiment) {
        if (sentiment > 0) {
          return "rgb(" + (1 - sentiment) * 255 + ", 255 , 0)";
        } else {
          return "rgb(255, "  + (1 + sentiment) * 255 + ", 0)";
        }
      }

      map.selectAll("circle")
          .remove();

      const bubbles = map.selectAll("myCircles")
          .data(tweets)
          .enter()
          .append("circle")
          .attr("cx", function (d) {
            return proj([d.coords[1], d.coords[0]])[0]
          })
          .attr("cy", function (d) {
            return proj([d.coords[1], d.coords[0]])[1]
          })
          .attr("r", 7)
          .style("fill", function (d) {
            return computeSentimentColor(d.score)
          })
          .attr("stroke", "#777777")
          .attr("stroke-width", 1)
          .attr("fill-opacity", 0.5);

      // Show tooltips when hovering over the features
      // Use "mousemove" instead of "mouseover" to update the tooltip
      // position when moving the cursor inside the feature.
      bubbles.on('mousemove', showTooltip)
          .on('mouseout', hideTooltip);
    })});
}

/**
 * Show a tooltip with details of a feature, e.g. when hovering over a
 * feature on the map.
 *
 * @param {Feature} d - The feature
 * @param {Number} i - The ID of the feature
 */
function showTooltip(d, i) {
  // Get the current mouse position (as integer)
  var mouse = d3.mouse(map.node()).map(function(d) { return parseInt(d); });

  // Calculate the absolute left and top offsets of the tooltip. If the
  // mouse is close to the right border of the map, show the tooltip on
  // the left.
  // To calculate the offsest, it is necessary to use the current size
  // of the map in proportion to the original size.
  var currentWidth = $('#map').width();
  var currentHeight = $('#map').height();
  var mouseL = mouse[0] * currentWidth / width;
  var mouseT = mouse[1] * currentHeight / height;
  var left = Math.min(currentWidth-12*getName(d).length, (mouseL+20));
  var top = Math.min(currentHeight-40, (mouseT+20));

  // Populate the tooltip, position it and show it
  tooltip.classed("hidden", false)
      .attr("style", "left:"+left+"px;top:"+top+"px")
      .html([
        '<strong>', d.user, '</strong><br/>',
        '<div style="color:blue">@', d.screen_name, '</div>',
        d.text,
      ].join(''));
}


/**
 * Hide the tooltip.
 */
function hideTooltip() {
  tooltip.classed("hidden", true);
}


/**
 * Helper function to access the property of the feature used as value.
 *
 * @param {Feature} f
 * @return {Number} value
 */
function getValue(f) {
  if (f.properties) {
    return +f.properties[day];
  } else {
    return 0;
  }
}


/**
 * Helper function to access the property of the feature used as name or
 * label.
 *
 * @param {Feature} f
 * @return {String} name
 */
function getName(f) {
  if (f.properties) {
    return f.properties.Name;
  } else {
    return "Tweet";
  }
}


/**
 * Format a number: Add thousands separator.
 * http://stackoverflow.com/a/2901298/841644
 */
function formatNumber(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "'");
}
