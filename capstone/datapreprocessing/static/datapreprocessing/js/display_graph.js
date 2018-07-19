$(function() {

    const display = $("tr.display");

    console.log('asd');
    display.click(function() {

        $('html, body').animate({ scrollTop: $(document).height()}, 1000);


        const data = $(this).attr("data-value");
        var json_data = $(this).attr("data-variables");
        const parsed = JSON.parse(data);

        const field = $(this).children(".point").html();
        const source = $(this).children(".source").html();

        var time = 'Yearly';
        var categories = [];
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
                data: withForecast

            }]
        });

        var json_variables = JSON.parse(json_data);
        json_variables = json_variables.variables;
        const table = $("#table");
        table.empty();

        var header = '<div class="card-header no-border" style="text-align: center;"><h3 class="card-title">' + field  + '</h3></div>';
        var tb = '<div class="card-body"><table class="table table-bordered" id="data-here">' +
            '<thead>' +
            '<tr>' +
            '<th>Category</th><th>Score</th><th>Remark</th>' +
            '</tr>' +
            '</thead>' +
            '</table>' +
            '</div>';

        table.append(header);
        table.append(tb);

        var row = "";

        for (var x in json_variables) {
            row += '<tr><td>' + json_variables[x].category + '</td><td>' + json_variables[x].score + '</td>' +
                '<td>'+ json_variables[x].remark +'</td></tr>';
        }

        $("#data-here").append(row);

    });
});