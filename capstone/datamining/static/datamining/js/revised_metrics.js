$(function() {

    $("#viewCorrelationGraph").on("show.bs.modal", function(e) {

        const button = $(e.relatedTarget);
        const field = button.parent().siblings(".field").html();
        const source = button.parent().siblings(".source").html();

        $.ajax({
            url: "/data-mining/get_variables_v2",
            type: "post",
            data: {
                'source': source,
                'field': field
            },
            dataType: "json",
            success: function(d) {

                console.log(d);

                $(".holder").remove();

                const callbackLength = d.variables.length;
                var division;
                const div = $("#scatterGraph").children(".row");
                const thresholdBtn = $("#btnThreshold");

                var independent = [];

                switch (callbackLength) {
                    case 3: division = 4; break;
                    case 2: division = 6; break;
                    case 1: division = 12; break;
                    default: division = 0;
                }

                for (var x = 0; x < callbackLength; x++) {
                    var html = '<div class="graphsHere"></div>';
                    div.append(html);
                }

                const graphsHere = $(".graphsHere");

                graphsHere.each(function(index) {
                    $(this).attr('class', 'holder col-' + division);
                    $(this).attr('id', 'holder' + index)
                });

                $(".holder").each(function(index) {
                    $(this).append(Highcharts.chart('holder' + index, {
                        chart: {
                            type: 'scatter',
                            zoomType: 'xy'
                        },
                        title: {
                            text: d.variables[index].category + ' vs. ' + field
                        },
                        xAxis: {
                            title: {
                                enabled: true,
                                text: field
                            },
                            startOnTick: true,
                            endOnTick: true,
                            showLastLabel: true
                        },
                        yAxis: {
                            title: {
                                text: d.variables[index].category
                            }
                        },
                        legend: {
                            layout: 'vertical',
                            align: 'left',
                            verticalAlign: 'top',
                            x: 100,
                            y: 70,
                            floating: true,
                            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
                            borderWidth: 1
                        },
                        plotOptions: {
                            scatter: {
                                marker: {
                                    radius: 5,
                                    states: {
                                        hover: {
                                            enabled: true,
                                            lineColor: 'rgb(100,100,100)'
                                        }
                                    }
                                },
                                states: {
                                    hover: {
                                        marker: {
                                            enabled: false
                                        }
                                    }
                                },
                                tooltip: {
                                    headerFormat: '<b>{series.name}</b><br>',
                                    pointFormat: '{point.x} , {point.y}'
                                }
                            }
                        },
                        series: [{
                            name: 'Observation',
                            color: 'rgba(119, 152, 191, .5)',
                            data: d.variables[index].variables
                        }]
                    }));
                });


                thresholdBtn.attr("data-values", JSON.stringify(d));
                thresholdBtn.attr("data-field", field);
            },
            error: function(e) {
                console.log(e.responseText);
            }
        });
    });

    $("#setThreshold").on("show.bs.modal", function(e) {

        $("#viewCorrelationGraph").modal('hide');

        const button = $(e.relatedTarget);
        const values = JSON.parse(button.attr("data-values"));
        const field = button.attr("data-field");

        const v = values.variables[0].variables;
        const variables = [];

        $("b#field").html(field);

        for (var x in v) {
            variables.push(v[x][0]);
        }

        const forecast = parseFloat(get_weighted_moving_average(variables));
        const attribute = {
            'field': field,
            'values': values
        };

        const withForecast = variables.slice();
        withForecast.push({
            'y': forecast,
            'color': '#daffc4'
        });

        $("button#addMetric").attr("data-core", JSON.stringify(attribute));

        Highcharts.chart('averageValues', {
            chart: {
                type: 'column'
            },
            title: {
                text: "Yearly Totals of " + field
            },
            xAxis: {
                categories: cheatYears(v.length),
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Population'
                },
                plotLines: [{
                    value: getAverage(variables),
                    color: 'green',
                    width: 2,
                    label: {
                        text: 'Average = ' + getAverage(variables)
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
    });





    $("button#addMetric").click(function() {

        const core = JSON.parse($(this).attr("data-core"));
        console.log(core);

        const threshold = $("#threshold").val();
        const isBad = $("#high").val();
        const metric = core.values.source + " | " + core.field;

        if (threshold === '') {
            alert("Please input a value");
        }
        else {
            $.ajax({
                url: "/data-pre_processing/ajax/add_metric",
                type: "post",
                data: {
                    'metric': metric,
                    'is_bad': isBad,
                    'threshold': threshold,
                    'jsonData': JSON.stringify(core.values)
                },
                success: function() {
                    alert("Metric successfully added");
                    window.location.replace('/data-pre_processing');
                },
                error: function(d) {
                    console.log(d.responseText);
                }
            });
        }


    });
});


function cheatYears(length) {

    var yearNow = moment().year() - 1;
    var years = [yearNow];

    for (var x = 0; x < length - 1; x++) {
        yearNow--;
        years.push(yearNow);
    }

    years.push(moment().year());
    console.log(years.sort());
    return years.sort();
}

function getAverage(values) {

    if (values.length === 0) {
        return 0;
    }

    var sum = 0;
    for (var x in values) {
        sum = sum + parseFloat(values[x]);
    }

    return parseFloat((sum / values.length).toFixed(3));
}

function get_weights(n) {

    var weights = [];

    var sum = 0;
    for (var x = 1; x <= n; x++) {
        sum += x;
    }

    for (var i = 1; i <= n; i++) {
        console.log(i / sum);
        weights.push(i / sum);
    }

    console.log(weights);
    return weights;
}

function get_weighted_moving_average(data) {

    const length = data.length;
    const weights = get_weights(length);

    sum = 0;
    for (var x = 0; x < length; x++) {
        sum += (data[x] * weights[x]);
    }

    return sum.toFixed(2);
}

































function getCookie(name) {

    var cookieValue = null;

    if (document.cookie && document.cookie != '') {

        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});