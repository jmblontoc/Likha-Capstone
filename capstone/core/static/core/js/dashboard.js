$(function() {
    console.log("qwe");

    $.ajax({
        url: "/ajax/dashboard",
        dataType: "json",
        success: function(data) {
            console.log(data);

            Highcharts.chart('micro-dashboard', {
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Micronutrient Supplementation Given for the Last 3 Months'
                },

                xAxis: {
                    categories: data.micro.months,
                    crosshair: true
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Population'
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                        '<td style="padding:0"><b>{point.y:.1f} </b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0
                    }
                },
                series: data.micro.values
            });

            const date = moment().format("LL");

            // Highcharts.chart('maternal-dash', {
            //     chart: {
            //     type: 'column'
            //   },
            //   title: {
            //     text: 'Maternal Care as of ' + date
            //   },
            //   xAxis: {
            //     categories: data.maternal.fields,
            //     crosshair: true
            //   },
            //   yAxis: {
            //     min: 0,
            //     title: {
            //       text: 'Population'
            //     }
            //   },
            //   tooltip: {
            //     headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            //     pointFormat: '<tr><td style="color:{series.color};padding:0">Total: </td>' +
            //       '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
            //     footerFormat: '</table>',
            //     shared: true,
            //     useHTML: true
            //   },
            //   plotOptions: {
            //     column: {
            //       pointPadding: 0.2,
            //       borderWidth: 0
            //     }
            //   },
            //   series: [{
            //     name: 'Fields',
            //     data: data.maternal.values
            //
            //   }]
            // });


            Highcharts.chart('childcare-dash', {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Illnesses of Children as of ' + date
                },

                xAxis: {
                    categories: data.child_care.fields,
                    title: {
                        text: null
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Population',
                        align: 'high'
                    },
                    labels: {
                        overflow: 'justify'
                    }
                },
                tooltip: {
                    valueSuffix: ' millions'
                },
                plotOptions: {
                    bar: {
                        dataLabels: {
                            enabled: true
                        }
                    }
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'top',
                    x: -40,
                    y: 80,
                    floating: true,
                    borderWidth: 1,
                    backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
                    shadow: true
                },
                credits: {
                    enabled: false
                },
                series: [{
                    name: 'Disease',
                    data: data.child_care.values
                }]
            });


            // Build the chart
            // Highcharts.chart('socio-dash', {
            //     chart: {
            //         plotBackgroundColor: null,
            //         plotBorderWidth: null,
            //         plotShadow: false,
            //         type: 'pie'
            //     },
            //     title: {
            //         text: 'Milk Feeding Practices in Families as of ' + date
            //     },
            //     tooltip: {
            //         pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            //     },
            //     plotOptions: {
            //         pie: {
            //             allowPointSelect: true,
            //             cursor: 'pointer',
            //             dataLabels: {
            //                 enabled: false
            //             },
            //             showInLegend: true
            //         }
            //     },
            //     series: [{
            //         name: 'Method',
            //         colorByPoint: true,
            //         data: data.socioeconomic.feeding
            //     }]
            // });
        },
        error: function(e) {
            console.log(e.responseText);
        }
    });


});