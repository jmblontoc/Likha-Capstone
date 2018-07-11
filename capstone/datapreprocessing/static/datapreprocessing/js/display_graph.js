$(function() {

    const display = $("tr.display");

    display.click(function() {

        const data = $(this).attr("data-value");
        const parsed = JSON.parse(data);

        const field = $(this).children(".point").html();
        const source = $(this).children(".source").html();

        var time;
        if (source === 'Maternal Care' || source === 'Child Care') {
            time = "Monthly";
        }
        else {
            time = "Yearly";
        }

        var categories = [];
        var values = [];
        for (var x in parsed) {
            categories.push(x);
            values.push(parsed[x]);
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
                categories: categories,
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
            series: [{
                name: field,
                data: values

            }]
        });

        const table = $("#table");
        table.empty();

        var header = '<h4>' + field + " " + time + '</h4>';
        var tb = '<table class="table table-bordered" id="data-here">' +
            '<thead>' +
            '<tr>' +
            '<th>Time</th><th>Value</th>' +
            '</tr>' +
            '</thead>' +
            '</table>';

        table.append(header);
        table.append(tb);

        var row = "";

        for (var x in categories) {
            row += '<tr><td>' + categories[x] + '</td><td>' + values[x] + '</td>/tr>';
        }

        $("#data-here").append(row);

    });
});