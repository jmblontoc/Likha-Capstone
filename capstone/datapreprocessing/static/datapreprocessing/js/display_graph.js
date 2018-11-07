$(function() {

    const display = $("tr.display");

    console.log('asd');
    display.click(function() {

        $('html, body').animate({ scrollTop: $(document).height()}, 1000);


        const data = $(this).attr("data-value");
        var json_data = $(this).attr("data-variables");
        const parsed = JSON.parse(data);
        const prev = $(this).attr("data-prevalence");
        const prevLast = $(this).data("prevalenceLast");

        const field = $(this).children(".point").html();
        const source = $(this).children(".source").html();

        var time = 'Yearly';
        var categories = [];
        console.log(parsed);
        var values = [];
        for (var x in parsed) {
            categories.push(x);
            values.push(parsed[x]);
        }

        console.log(values);

        var withForecast = values.slice();

        const wma = parseFloat(get_weighted_moving_average(values));
        withForecast.push({'y': wma, 'color': '#daffc4'});
        console.log(withForecast);

        Highcharts.SVGRenderer.prototype.symbols.line = function(x, y, w, h) {
          return ['M', x, y, 'L', x + w, y];
        };

        if (Highcharts.VMLRenderer) {
            Highcharts.VMLRenderer.prototype.symbols.line = Highcharts.SVGRenderer.prototype.symbols.line;
        }


        $("#graph").empty();
        Highcharts.chart('graph', {

            chart: {
                type: 'column'
            },
            title: {
                text: field + " " + time
            },
            xAxis: {
                categories: cheatYears(values.length),
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Population'
                },
                plotLines: [{
                    value: getAverage(values),
                    color: 'green',
                    width: 2,
                    label: {
                        text: 'Average = ' + getAverage(values)
                    },
                    zIndex: 4
                }]
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
            series: [{
                name: field,
                data: withForecast,
                marker: {
                    symbol: 'cross',
                    lineColor: null,
                    lineWidth: 2
                }

            }, {
                name: 'Predicted Value',
                data: [],
                color: '#daffc4'
            }]
        });

        const div = $("#table");
        div.empty();
        div.append("<p class='text-center' style='padding-top: 180px;'>Prevalence Rate for " + moment().year() + "</p><h1 class='display-4 text-center'>" + prev + "%</h1>");
        div.append("<h3 class='text-center mt-5' style='font-weight:normal'><span style='font-weight: 500;'>" + prevLast +"%</span> <span>in " + parseInt(moment().year() - 1) +"</span></h3>");


    });
});