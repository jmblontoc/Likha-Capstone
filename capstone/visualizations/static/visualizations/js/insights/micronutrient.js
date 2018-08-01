$(function() {

    $.ajax({
        url: "/visualizations/ajax_top3_mns",
        success: function(e) {
            console.log(e);

            Highcharts.chart('totals', {
                colors: ['#014b90','#4078ac','#80a5c8'],
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Barangays with the Highest Number of Micronutrient Supplementation'
                },
                xAxis: {
                    categories: e.highest.barangays
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
                    data: e.highest.vitaminA
                }, {
                    name: 'Iron',
                    data: e.highest.iron
                }, {
                    name: 'Micronutrient Powder',
                    data: e.highest.mnp
                }]
            });

            Highcharts.chart('totals-lowest', {
                colors: ['#014b90','#4078ac','#80a5c8'],
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Barangays with the Lowest Number of Micronutrient Supplementation'
                },
                xAxis: {
                    categories: e.lowest.barangays
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
                    data: e.lowest.vitaminA
                }, {
                    name: 'Iron',
                    data: e.lowest.iron
                }, {
                    name: 'Micronutrient Powder',
                    data: e.lowest.mnp
                }]
            });
        },
        error: function(e) {
            console.log(e.responseText);
        }
    });
});