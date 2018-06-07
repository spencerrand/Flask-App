///////////////////////////////////////////////
// Initialize                                //
///////////////////////////////////////////////

function init(){

  showMetadata("BB_940");
  showPieChart("BB_940");
  showBubbleChart("BB_940");

}

///////////////////////////////////////////////
// Get Sample Names                          //
///////////////////////////////////////////////

function getNames() {

  Plotly.d3.json("/names", function(error, response) {
      
    // Get selection element from HTML
    var selDataset = document.getElementById("selDataset");

    // Loop through the response
    for (i = 0; i < response.length; i++){

      // Create a new option element
      var option = document.createElement("option");

      // Add the sample ID as both the text and value
      option.text = response[i];
      option.value = response[i];

      // Append the new element
      selDataset.appendChild(option);        
    }

  });
  
}

///////////////////////////////////////////////
// Show Metadata                             //
///////////////////////////////////////////////

function showMetadata(sample){
  
  Plotly.d3.json(`/metadata/${sample}`, function(error, response) {

    // Get the panel element from HTML
    var panelMetadata = document.getElementById("panelMetadata");

    // Clear out the text in the panel
    panelMetadata.innerHTML = "";

    // Loop through each key in the dictionary
    for (var key in response){

      // Add "KEY: VALUE" as a line item to the panel
      panelMetadata.innerHTML += key + ": " + response[key] + "<br>";   
    }
  }); 

}

///////////////////////////////////////////////
// Show Bubble Chart                         //
///////////////////////////////////////////////

function showBubbleChart(sample){

  Plotly.d3.json(`/samples/${sample}`, function(error, response) {

    var otuIDs = response['otu_ids'];
    var sampleValues = response['sample_values'];

    var trace = [{
      x: otuIDs,
      y: sampleValues,
      mode: "markers",
      marker: { 
        size: sampleValues,
        color: otuIDs
      }
    }];

    var layout = {
      height: 600,
      width: 1100
    }

    Plotly.plot("bubble", trace, layout);
    
  }); 

}

///////////////////////////////////////////////
// Update Bubble Chart                       //
///////////////////////////////////////////////

function updateBubbleChart(sample){
  
  Plotly.d3.json(`/samples/${sample}`, function(error, response) {

    var otuIDs = response['otu_ids'];
    var sampleValues = response['sample_values'];

    var Bubble = document.getElementById("bubble");
    Plotly.restyle(Bubble, "x", [otuIDs]);
    Plotly.restyle(Bubble, "y", [sampleValues]);

  });

}

///////////////////////////////////////////////
// Show Pie Chart                            //
///////////////////////////////////////////////

function showPieChart(sample){

  Plotly.d3.json(`/samples/${sample}`, function(error, response) {

    var pieValues = response['sample_values'].slice(0,10);
    var pieLabels = response['otu_ids'].slice(0,10);

    var data = [{
      values: pieValues,
      labels: pieLabels,
      type: "pie",
      hoverinfo: 'label'
    }];

    var layout = {
      height: 600,
      width: 800
    };

    Plotly.plot("pie", data, layout);

    // var PIE = document.getElementById("pie");
    // Plotly.restyle(PIE, "hoverinfo", ['q','w','e','r','t','y','u','i','o','p']);

    // Plotly.d3.json(`/otu`, function(error, response) {
      
    //   pieHoverText = [];
    //   for (i = 0; i < 10; i++){
    //     pieHoverText.push(response[pieLabels[i]])
    //   }
      
    //   var PIE = document.getElementById("pie");
    //   Plotly.restyle(PIE, "text", [pieHoverText]);
    // }); 
    
  }); 

}

///////////////////////////////////////////////
// Update Pie Chart                          //
///////////////////////////////////////////////

function updatePieChart(sample){
  
  Plotly.d3.json(`/samples/${sample}`, function(error, response) {

    var newValues = response['sample_values'].slice(0,10);
    var newLabels = response['otu_ids'].slice(0,10);

    var PIE = document.getElementById("pie");
    Plotly.restyle(PIE, "values", [newValues]);
    Plotly.restyle(PIE, "labels", [newLabels]);

  });

}

///////////////////////////////////////////////
// Dropdown Option Changed                   //
///////////////////////////////////////////////

function optionChanged(sample){
  
  showMetadata(sample);
  updatePieChart(sample);
  updateBubbleChart(sample);

}

getNames();
init();