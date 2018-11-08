function buildMetadata(sample) {
  d3.json(`/metadata/${sample}`).then(function(data)
   {
    var PANE = d3.select("#sample-metadata");

    // Use `.html("") to clear any existing metadata
    PANE.html("");

    Object.entries(data).forEach(([key, value]) => {
      PANE.append("h6").text(`${key}: ${value}`);
    });

  });
}

function buildCharts(sample) {
  d3.json(`/samples/${sample}`).then((data) => {
    var ids = data.otu_ids;
    var labels = data.otu_labels;
    var sample_values = data.sample_values;

    // Build a Bubble Chart
    var layout = {
      margin: { t: 0 },
      hovermode: "closest",
      xaxis: { title: "ID" }
    };
    var data = [
      {
        x: ids,
        y: sample_values,
        text: labels,
        mode: "markers",
        marker: {
          size: sample_values,
          color: ids,
          colorscale: "Earth"
        }
      }
    ];

    Plotly.plot("bubble", data, layout);

    // Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
    var data2 = [
      {
        values: sample_values.slice(0, 10),
        labels: otu_ids.slice(0, 10),
        type: "pie",
        hovertext: otu_labels.slice(0, 10),
        hoverinfo: "hovertext",
      }
    ];

    var layout2 = {
      margin: { t: 0, l: 0 }
    };

    Plotly.plot("pie", data2, layout2);
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var dropdown = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((s_names) => {
    consol.log(s_names);
    s_names.forEach((name) => {
      dropdown.append("option").text(name).property("value", name);
    });

    // Use the first sample from the list to build the initial plots
    var ex_sample = s_names[0];
    buildCharts(ex_sample);
    buildMetadata(ex_sample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
