$(function() {
    console.log("qwe");

    $.ajax({
        url: "/ajax/dashboard/micronutrient",
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
                    categories: data.months,
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
                series: data.values
            });
        },
        error: function(e) {
            console.log(e.responseText);
        }
    });


});