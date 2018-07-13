$(function() {

    console.log("wew");

    Highcharts.chart('totals', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Barangays with the Highest Number of Micronutrient Supplementation'
        },
        xAxis: {
            categories: ['Barangay Poblacion', 'Barangay Ibaba', 'Barangay Addition Hills', 'Burol', 'Daang Bakal']
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total'
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
            name: 'Vitamin A',
            data: [15, 23, 14, 21, 24]
        }, {
            name: 'Iron',
            data: [21, 22, 31, 31, 38]
        }, {
            name: 'Micronutrient Powder',
            data: [23, 14, 14, 27, 12]
        }]
    });

    Highcharts.chart('totals-lowest', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Barangays with the Lowest Number of Micronutrient Supplementation'
        },
        xAxis: {
            categories: ['Barangay Poblacion', 'Barangay Ibaba', 'Barangay Addition Hills', 'Burol', 'Daang Bakal']
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Total'
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
            name: 'Vitamin A',
            data: [5, 3, 4, 1, 4]
        }, {
            name: 'Iron',
            data: [1, 2, 1, 3, 8]
        }, {
            name: 'Micronutrient Powder',
            data: [3, 4, 4, 7, 2]
        }]
    });
});