/**
 * Lukas Vonlanthen (2015)
 * lukas.vonlanthen[at]cde.unibe.ch
 *
 * Code inspired by:
 * - http://prag.ma/code/d3-cartogram/
 * - http://techslides.com/demos/d3/worldmap-template.html
 *
 * Data sources:
 * - http://www.pxweb.bfs.admin.ch/?px_language=en
 * - http://www.bfs.admin.ch/bfs/portal/de/index/dienstleistungen/geostat/datenbeschreibung/generalisierte_gemeindegrenzen.html
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
    stat = d3.select("#status"),
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

// Define the zoom and attach it to the map
var zoom = d3.behavior.zoom()
    .scaleExtent([1, 10])
    .on('zoom', doZoom);
map.call(zoom);

// Define the projection of the map (center and scale will be defined
// later)
var proj = d3.geo.mercator();

// Prepare the cartogram
var topology,
    geometries,
    dataById = {},
    carto = d3.cartogram()
        .projection(proj)
        .properties(function(d) {
          if (!dataById[d.properties.KTNR]) {
            console.log('ERROR: Entry "' + d.properties.KTNR + '" was found in the Topojson but not in the data CSV. Please correct either of them.');
          }
          // Add the cartogram data as property of the cartogram features
          return dataById[d.properties.KTNR];
        });

// Define the fields of the data
var fields = [
      {name: "(no scale)", id: "none"},
      {name: "Total Population", id: "pop_total", key: "pop_%d"},
      {name: "Female Population", id: "pop_female", key: "female_%d"},
      {name: "Male Population", id: "pop_male", key: "male_%d"},
      {name: "Swiss Population", id: "pop_swiss", key: "ch_%d"},
      {name: "Foreign Population", id: "pop_foreign", key: "foreign_%d"},
    ],
    years = [1971, 1981, 1991, 2001, 2010],
    fieldsById = d3.nest()
        .key(function(d) { return d.id; })
        .rollup(function(d) { return d[0]; })
        .map(fields),
    field = fields[0],
    year = years[0],
    currentKey;

// Define the dropdown to select a field to scale by.
var fieldSelect = d3.select("#field")
    .on("change", function(e) {
      // On change, update the URL hash
      field = fields[this.selectedIndex];
      location.hash = "#" + [field.id, year].join("/");
    });
// Populate its options with the fields available
fieldSelect.selectAll("option")
    .data(fields)
    .enter()
    .append("option")
    .attr("value", function(d) { return d.id; })
    .text(function(d) { return d.name; });

// Define the dropdown to select a year.
var yearSelect = d3.select("#year");

// D3's "change" event is somehow not triggered when selecting the
// dropdown value programmatically. Use jQuery's change event instead.
$('#year').on("change", function(e) {
  // On change, update the URL hash
  year = years[this.selectedIndex];
  location.hash = "#" + [field.id, year].join("/");
});

// Populate its options with the years available
yearSelect.selectAll("option")
    .data(years)
    .enter()
    .append("option")
    .attr("value", function(y) { return y; })
    .text(function(y) { return y; })

// Define some variables needed for the play functionality
var isPlaying,
    outerIsPlaying, innerIsPlaying;

// Define what happens when the play buttons are clicked
var playButton = $('#play');
var stopButton = $('#stop');
playButton.on('click', function() {
  stop_play();
  playButton.prop('disabled', true);
  stopButton.prop('disabled', false);
  isPlaying = true;
  play_inner();
})
stopButton.on('click', function() {
  playButton.prop('disabled', false);
  stopButton.prop('disabled', true);
  stop_play();
});

function stop_play() {
  isPlaying = false;
  clearTimeout(innerIsPlaying);
  clearTimeout(outerIsPlaying);
}

/**
 * Recursive function to loop infinitively through the fields in the
 * year dropdown.
 *
 * Caution: This function has no exit, it does not stop by itself!
 */
function play_inner() {
  $('#year>option').each(function(i) {
    var el = $(this);
    innerIsPlaying = setTimeout(function() {
      if (isPlaying) {
        // Trigger a change event
        el.prop("selected", true).change();
      }
    }, i * 2000);
  });
  outerIsPlaying = setTimeout(function() {
    play_inner();
  }, years.length * 2000);
}

// Add a listener to the change of the URL hash
window.onhashchange = function() {
  parseHash();
};

// Read the geometry data
d3.json("ch_cantons.topojson", function(topo) {
  topology = topo;

  // The mapped unit for cantons: Cantons
  geometries = topology.objects.cantons.geometries;

  // Read the data for the cartogram
  d3.csv("ch_population.csv", function(data) {

    // Prepare a function to easily access the data by its ID
    // "ID" for cantons: KTNR
    dataById = d3.nest()
        .key(function(d) { return parseInt(d.KTNR); })
        .rollup(function(d) { return d[0]; })
        .map(data);

    // Initialize the map
    init();
  });
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

  // Show tooltips when hovering over the features
  // Use "mousemove" instead of "mouseover" to update the tooltip
  // position when moving the cursor inside the feature.
  mapFeatures.on('mousemove', showTooltip)
      .on('mouseout', hideTooltip);

  // Parse the URL hash to see if the map was loaded with a cartogram
  parseHash();
}

/**
 * Reset the cartogram and show the features without scaling.
 */
function reset() {

  // Reset the calculation statistics text
  stat.text("");

  // Create the cartogram features (without any scaling)
  var cartoFeatures = carto.features(topology, geometries),
      path = d3.geo.path()
          .projection(proj);

  // Redraw the features with a transition
  mapFeatures.data(cartoFeatures)
      .transition()
      .duration(750)
      .ease("linear")
      .attr("fill", "#ddd")
      .attr("d", path);
}

function update() {

  // Keep track of the time it takes to calculate the cartogram
  var start = Date.now();

  // Update the current key
  currentKey = field.key.replace("%d", year);

  // Prepare the values and determine minimum and maximum values
  var value = function(d) {
        return getValue(d);
      },
      values = mapFeatures.data()
          .map(value)
          .filter(function(n) {
            return !isNaN(n);
          })
          .sort(d3.ascending),
      lo = values[0],
      hi = values[values.length - 1];

  // Determine the colors within the range
  var color = d3.scale.linear()
      .range(colors)
      .domain(lo < 0
          ? [lo, 0, hi]
          : [lo, d3.mean(values), hi]);

  // Normalize the scale to positive numbers
  var scale = d3.scale.linear()
      .domain([lo, hi])
      .range([1, 1000]);

  // Tell the cartogram to use the scaled values
  carto.value(function(d) {
    return scale(value(d));
  });

  // Generate the new features and add them to the map
  var cartoFeatures = carto(topology, geometries).features;
  mapFeatures.data(cartoFeatures);

  // Scale the cartogram with a transition
  mapFeatures.transition()
      .duration(750)
      .ease("linear")
      .attr("fill", function(d) {
        return color(value(d));
      })
      .attr("d", carto.path);

  // Show the calculation statistics and hide the update indicator
  var delta = (Date.now() - start) / 1000;
  stat.text(["calculated in", delta.toFixed(1), "seconds"].join(" "));
  hideUpdateIndicator();
}


/**
 * Use a deferred function to update the cartogram. This allows to set a
 * timeout limit.
 */
var deferredUpdate = (function() {
  var timeout;
  return function() {
    var args = arguments;
    clearTimeout(timeout);
    stat.text("calculating...");
    return timeout = setTimeout(function() {
      update.apply(null, arguments);
    }, 10);
  };
})();


/**
 * Parse the URL hash location to determine whether to show features
 * scaled or not.
 */
function parseHash() {

  // Extract the field and year from the URL hash
  var parts = location.hash.substr(1).split("/"),
      desiredFieldId = parts[0],
      desiredYear = +parts[1];

  // Make sure field and year are valid, else use the defaults
  field = fieldsById[desiredFieldId] || fields[0];
  year = (years.indexOf(desiredYear) > -1) ? desiredYear : years[0];

  // Mark the field as selected in the dropdown
  fieldSelect.property("selectedIndex", fields.indexOf(field));

  if (field.id === "none") {
    // If no scale is used, disable the year dropdown and the play
    // button
    yearSelect.attr("disabled", "disabled");
    playButton.prop('disabled', true);
    reset();
  } else {
    if (!isPlaying) {
      playButton.prop('disabled', false);
    }
    // If year is selected, mark it as selected in the dropdown
    if (field.years) {
      if (field.years.indexOf(year) === -1) {
        year = field.years[0];
      }
      yearSelect.selectAll("option")
          .attr("disabled", function(y) {
            return (field.years.indexOf(y) === -1) ? "disabled" : null;
          });
    } else {
      yearSelect.selectAll("option")
          .attr("disabled", null);
    }

    yearSelect
        .property("selectedIndex", years.indexOf(year))
        .attr("disabled", null);

    deferredUpdate();
    location.replace("#" + [field.id, year].join("/"));
  }
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
        '<strong>', getName(d), '</strong><br/>',
        'Population: ', formatNumber(getValue(d)),
      ].join(''));
}


/**
 * Hide the tooltip.
 */
function hideTooltip() {
  tooltip.classed("hidden", true);
}


/**
 * Zoom the features on the map.
 */
function doZoom() {

  // Zoom and keep the stroke width proportional
  mapFeatures.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")").style("stroke-width", .5 / d3.event.scale + "px");

  // Hide the tooltip after zooming
  hideTooltip();
}


/**
 * Show an update indicating while calculating the cartogram.
 */
function showUpdateIndicator() {
  body.classed("updating", true);
}


/*
 * Hide the update indicator after the cartogram was calculated.
 */
function hideUpdateIndicator() {
  body.classed("updating", false);
}


/**
 * Helper function to access the property of the feature used as value.
 *
 * @param {Feature} f
 * @return {Number} value
 */
function getValue(f) {
  return +f.properties[currentKey];
}


/**
 * Helper function to access the property of the feature used as name or
 * label.
 *
 * @param {Feature} f
 * @return {String} name
 */
function getName(f) {
  return f.properties.Name;
}


/**
 * Format a number: Add thousands separator.
 * http://stackoverflow.com/a/2901298/841644
 */
function formatNumber(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, "'");
}
