// from data.js
var tableData = data;

// Use D3 to select the table body
var tbody = d3.select("tbody");
var button = d3.select("#filter-btn")

//Create the full table
tableData.forEach(sighting => {
  row = tbody.append("tr");
  row.append("td").text(sighting.datetime);
  row.append("td").text(sighting.city);
  row.append("td").text(sighting.state);
  row.append("td").text(sighting.country);
  row.append("td").text(sighting.shape);
  row.append("td").text(sighting.durationMinutes);
  row.append("td").text(sighting.comments);
});

button.on("click", function() {
  // Prevent the page from refreshing
  d3.event.preventDefault();

  // clear table data
  tbody.html("");

  var inputDate = d3.select("#datetime").property("value");
  var inputCity = d3.select("#city").property("value");
  var inputState = d3.select("#state").property("value");
  var inputCountry = d3.select("#country").property("value");
  var inputShape = d3.select("#shape").property("value");

  var filteredData = tableData.filter(sighting => sighting.datetime == inputDate && sighting.city == inputCity && sighting.state == inputState && sighting.country == inputCountry && sighting.shape == inputShape);

  filteredData.forEach(sighting => {
    row = tbody.append("tr");
    row.append("td").text(sighting.datetime);
    row.append("td").text(sighting.city);
    row.append("td").text(sighting.state);
    row.append("td").text(sighting.country);
    row.append("td").text(sighting.shape);
    row.append("td").text(sighting.durationMinutes);
    row.append("td").text(sighting.comments);
  })
});
