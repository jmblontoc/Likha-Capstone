$(function() {

    console.log("wew");

    Highcharts.chart('totals', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Barangays with Highest Number of Malnourished Children'
        },
        xAxis: {
            categories: ['Barangay Poblacion', 'Barangay Ibaba', 'Barangay Addition Hills', 'Burol', 'Daang Bakal']
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
            data: [5, 3, 4, 1, 4]
        }, {
            name: 'S + SS',
            data: [2, 2, 3, 3, 8]
        }, {
            name: 'W + SW',
            data: [3, 4, 4, 7, 2]
        }]
    });
});