$(function() {

    console.log("wew");

    $.ajax({
        url: "/visualizations/ajax_highest",
        success: function(e) {

        Highcharts.chart('totals', {
        colors: ['#014b90','#4078ac','#80a5c8'],
        chart: {
            type: 'column'
        },
        title: {
            text: 'Barangays with the Highest Number of Malnourished Children'
        },
        xAxis: {
            categories: e.barangays
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total fruit consumption'
            },
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                }
            }
        },
        legend: {
            align: 'right',
            x: -30,
            verticalAlign: 'top',
            y: 25,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || 'white',
            borderColor: '#CCC',
            borderWidth: 1,
            shadow: false
        },
        tooltip: {
            headerFormat: '<b>{point.x}</b><br/>',
            pointFormat: '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true,
                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white'
                }
            }
        },
        series: [{
            name: 'UW + SUW',
            data: e.first
        }, {
            name: 'S + SS',
            data: e.second
        }, {
            name: 'W + SW',
            data: e.third
        }]
    });
        },
        error: function(e) {
            console.log(e.responseText);
        }
    });
});