
am4core.ready(function() {

// Themes begin
// am4core.useTheme(am4themes_material);
// am4core.useTheme(am4themes_animated);
// Themes end

// Create chart
var chart = am4core.create("chartdiv", am4charts.XYChart);
chart.padding(0, 15, 0, 15);

// Load external data
var host_name = 'http://127.0.0.1:8001';

var stock_symbol = document.getElementById("stock_symbol").textContent;
console.log(stock_symbol);
params = {'stock_symbol': stock_symbol};

// $.ajaxSetup({  
//     async : false  
// });

$.get(host_name + '/new_data', params, function (data) {
    // console.log(data[0]);
    console.log('data', data);
    var res = JSON.parse(data);
    chart.data = res['chart'];
    // console.log('res', res);

    var pred = res['pred'];

    for(i=1; i<=4; i++){
        document.getElementById(`val_${i.toString()}`).textContent = pred[i-1][0];
        document.getElementById(`val_${i.toString()}_f`).textContent = pred[i-1][1];

        var par = document.getElementById(`val_${i.toString()}`).parentElement;
        if(pred[i-1][1] == 'Up'){
            par.classList.add('table-success');
        }else if(pred[i-1][1] == 'Down'){
            par.classList.add('table-danger');
        }
    }
});

    

//   var jsonObject = JSON.parse('{{ predicted_result_df | escapejs}}');
//   chart.data = jsonObject

// the following line makes value axes to be arranged vertically.
chart.leftAxesContainer.layout = "vertical";

// uncomment this line if you want to change order of axes
//chart.bottomAxesContainer.reverseOrder = true;

var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
dateAxis.renderer.grid.template.location = 0;
dateAxis.renderer.ticks.template.length = 8;
dateAxis.renderer.ticks.template.strokeOpacity = 0.1;
dateAxis.renderer.grid.template.disabled = true;
dateAxis.renderer.ticks.template.disabled = false;
dateAxis.renderer.ticks.template.strokeOpacity = 0.2;
dateAxis.renderer.minLabelPosition = 0.01;
dateAxis.renderer.maxLabelPosition = 0.99;
dateAxis.keepSelection = true;
dateAxis.minHeight = 30;

dateAxis.groupData = true;
dateAxis.minZoomCount = 5;

// these two lines makes the axis to be initially zoomed-in
// dateAxis.start = 0.7;
// dateAxis.keepSelection = true;

var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.tooltip.disabled = true;
valueAxis.zIndex = 1;
valueAxis.renderer.baseGrid.disabled = true;
// height of axis
valueAxis.height = am4core.percent(65);

valueAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
valueAxis.renderer.gridContainer.background.fillOpacity = 0.05;
valueAxis.renderer.inside = true;
valueAxis.renderer.labels.template.verticalCenter = "bottom";
valueAxis.renderer.labels.template.padding(2, 2, 2, 2);

//valueAxis.renderer.maxLabelPosition = 0.95;
valueAxis.renderer.fontSize = "0.8em"

var series = chart.series.push(new am4charts.LineSeries());
series.dataFields.dateX = "Date";
series.dataFields.valueY = "Close";
series.tooltipText = "Prediction Close: $ {valueY.value}";
series.to
series.name = "Prediction Value";
series.defaultState.transitionDuration = 0;
series.stroke = am4core.color("#dd70d0");

var series2 = chart.series.push(new am4charts.LineSeries());
series2.dataFields.dateX = "Date";
series2.dataFields.valueY = "Close2";
series2.tooltipText = "Real Close: $ {valueY.value}";
series2.name = "Real Value";
series2.defaultState.transitionDuration = 0;
// series2.stroke = am4core.color("#4BC0C0");

var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis2.tooltip.disabled = true;
// height of axis
valueAxis2.height = am4core.percent(35);
valueAxis2.zIndex = 3
// this makes gap between panels
valueAxis2.marginTop = 30;
valueAxis2.renderer.baseGrid.disabled = true;
valueAxis2.renderer.inside = true;
valueAxis2.renderer.labels.template.verticalCenter = "bottom";
valueAxis2.renderer.labels.template.padding(2, 2, 2, 2);
//valueAxis.renderer.maxLabelPosition = 0.95;
valueAxis2.renderer.fontSize = "0.8em"

valueAxis2.renderer.gridContainer.background.fill = am4core.color("#000000");
valueAxis2.renderer.gridContainer.background.fillOpacity = 0.05;

var series3 = chart.series.push(new am4charts.ColumnSeries());
    series3.dataFields.dateX = "Date";
    series3.dataFields.valueY = "Volume";
    series3.yAxis = valueAxis2;
    series3.tooltipText = "{valueY.value}";
    series3.name = "Volume";
    // volume should be summed
    series3.groupFields.valueY = "sum";
    series3.defaultState.transitionDuration = 0;
    series2.stroke = am4core.color("#4BC0C0");



chart.cursor = new am4charts.XYCursor();

var scrollbarX = new am4charts.XYChartScrollbar();
scrollbarX.series.push(series);
scrollbarX.marginBottom = 20;
scrollbarX.scrollbarChart.xAxes.getIndex(0).minHeight = undefined;
chart.scrollbarX = scrollbarX;


/**
 * Set up external controls
 */

// Date format to be used in input fields
var inputFieldFormat = "yyyy-MM-dd";

chart.legend = new am4charts.Legend();


document.getElementById("b1m").addEventListener("click", function() {
    resetButtonClass();
    var max = dateAxis.groupMax["day1"];
    var date = new Date(max);
    date.setMonth(date.getMonth() - 1);

    dateAxis.zoomToDates(
    date,
    new Date(max)
    );
    //this.className = "amcharts-input amcharts-input-selected";
});

document.getElementById("b3m").addEventListener("click", function() {
    resetButtonClass();
    var max = dateAxis.groupMax["day1"];
    var date = new Date(max);
    date.setMonth(date.getMonth() - 3);

    dateAxis.zoomToDates(
    date,
    new Date(max)
    );
    //this.className = "amcharts-input amcharts-input-selected";
});

document.getElementById("b6m").addEventListener("click", function() {
    resetButtonClass();
    var max = dateAxis.groupMax["day1"];
    var date = new Date(max);
    date.setMonth(date.getMonth() - 6);

    dateAxis.zoomToDates(
    date,
    new Date(max)
    );
    //this.className = "amcharts-input amcharts-input-selected";
});

document.getElementById("b1y").addEventListener("click", function() {
    resetButtonClass();
    var max = dateAxis.groupMax["week1"];
    var date = new Date(max);
    date.setFullYear(date.getFullYear() - 1);

    dateAxis.zoomToDates(
    date,
    new Date(max)
    );
    //this.className = "amcharts-input amcharts-input-selected";
});

document.getElementById("bytd").addEventListener("click", function() {
    resetButtonClass();
    var date = new Date(dateAxis.max);
    date.setMonth(0, 1);
    date.setHours(0, 0, 0, 0);
    dateAxis.zoomToDates(date, new Date(dateAxis.max));
    //this.className = "amcharts-input amcharts-input-selected";
});

document.getElementById("bmax").addEventListener("click", function() {
    resetButtonClass();
    dateAxis.zoom({start:0, end:1});
    //this.className = "amcharts-input amcharts-input-selected";
});

function resetButtonClass() {
    var selected = document.getElementsByClassName("amcharts-input-selected");
    for(var i = 0; i < selected.length; i++) {
    selected[i].className = "amcharts-input";
    }
}

dateAxis.events.on("selectionextremeschanged", function() {
    updateFields();
});

dateAxis.events.on("extremeschanged", updateFields);

function updateFields() {
    var minZoomed = dateAxis.minZoomed + am4core.time.getDuration(dateAxis.mainBaseInterval.timeUnit, dateAxis.mainBaseInterval.count) * 0.5;
    document.getElementById("fromfield").value = chart.dateFormatter.format(minZoomed, inputFieldFormat);
    document.getElementById("tofield").value = chart.dateFormatter.format(new Date(dateAxis.maxZoomed), inputFieldFormat);
}

document.getElementById("fromfield").addEventListener("keyup", updateZoom);
document.getElementById("tofield").addEventListener("keyup", updateZoom);

var zoomTimeout;
function updateZoom() {
    if (zoomTimeout) {
    clearTimeout(zoomTimeout);
    }
    zoomTimeout = setTimeout(function() {
    resetButtonClass();
    var start = document.getElementById("fromfield").value;
    var end = document.getElementById("tofield").value;
    if ((start.length < inputFieldFormat.length) || (end.length < inputFieldFormat.length)) {
        return;
    }
    var startDate = chart.dateFormatter.parse(start, inputFieldFormat);
    var endDate = chart.dateFormatter.parse(end, inputFieldFormat);

    if (startDate && endDate) {
        dateAxis.zoomToDates(startDate, endDate);
    }
    }, 500);
}

}); // end am4core.ready()