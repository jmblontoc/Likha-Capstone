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

            const date = new Date();

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
        },
        error: function(e) {
            console.log(e.responseText);
        }
    });


});