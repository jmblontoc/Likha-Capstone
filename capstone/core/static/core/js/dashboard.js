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

            const date = moment().format("LLLL");

            Highcharts.chart('maternal-dash', {
                chart: {
                type: 'column'
              },
              title: {
                text: 'Maternal Care as of ' + date
              },
              xAxis: {
                categories: data.maternal.fields,
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
                pointFormat: '<tr><td style="color:{series.color};padding:0">Total: </td>' +
                  '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
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
              series: [{
                name: 'Fields',
                data: data.maternal.values

              }]
            });

            Highcharts.chart('childcare-dash', {
                chart: {
                type: 'column'
              },
              title: {
                text: 'Child Care as of ' + date
              },
              xAxis: {
                categories: data.child_care.fields,
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
                pointFormat: '<tr><td style="color:{series.color};padding:0">Total: </td>' +
                  '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
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
              series: [{
                name: 'Fields',
                data: data.child_care.values

              }]
            });

            Highcharts.chart('salt', {

                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                },
                title: {
                    text: 'Families Using Iodized Salt ' + date
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: false
                        },
                        showInLegend: true
                    }
                },
                series: [{
                    name: 'Using Iodized Salt',
                    colorByPoint: true,
                    data: [{
                        name: 'Yes',
                        y: data.socioeconomic.is_using_salt,
                        sliced: true,
                        selected: true
                    }, {
                        name: 'No',
                        y: 100 - data.socioeconomic.is_using_salt
                    }]
                }]
            });

            Highcharts.chart('ebf', {

                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                },
                title: {
                    text: 'Families Practicing Exclusive Breastfeeding as of ' + date
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: false
                        },
                        showInLegend: true
                    }
                },
                series: [{
                    name: 'Using Iodized Salt',
                    colorByPoint: true,
                    data: [{
                        name: 'Yes',
                        y: data.socioeconomic.is_ebf,
                        sliced: true,
                        selected: true
                    }, {
                        name: 'No',
                        y: 100 - data.socioeconomic.is_ebf
                    }]
                }]
            });
        },
        error: function(e) {
            console.log(e.responseText);
        }
    });


});