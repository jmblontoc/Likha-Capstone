$(function() {



    $("#viewCorrelationGraph").on("show.bs.modal", function(e) {
        const button = $(e.relatedTarget);

        const category = button.parent().siblings(".category").html();
        const source = button.parent().siblings(".source").html();
        const field = button.parent().siblings(".field").html();


        $.ajax({
            url: "/data-mining/get_variables",
            type: "post",
            data: {
                'category': category,
                'source': source,
                'field': field
            },
            dataType: "json",
            success: function(d) {

                const variables = d.variables;
                const thresholdBtn = $("#btnThreshold");

                var independent = [];

                for (var x in variables) {
                    independent.push(variables[x][0]);
                }

                const values = JSON.stringify({
                    'values': independent
                });


                thresholdBtn.attr("data-values", values);
                thresholdBtn.attr("data-field", field);
                thresholdBtn.attr("data-source", source);

                Highcharts.chart('scatterGraph', {
                    chart: {
                        type: 'scatter',
                        zoomType: 'xy'
                    },
                    title: {
                        text: category + ' vs. ' + source
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
                            text: category
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
                        data: variables
                    }]
                });
            },
            error: function(e) {
                console.log(e.responseText);
            }
        });
    });

    $("#setThreshold").on("show.bs.modal", function(e) {

        const button = $(e.relatedTarget);

        const values = JSON.parse(button.attr("data-values"));
        const field = button.attr("data-field");
        const source = button.attr("data-source");

        $("b#field").html(field);

        const attribute = {
            'field': field,
            'source': source
        };

        $("button#addMetric").attr("data-core", JSON.stringify(attribute));

        Highcharts.chart('averageValues', {
            chart: {
                type: 'column'
            },
            title: {
                text: "Yearly Totals of " + field
            },
            xAxis: {
                categories: cheatYears(values.values.length),
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Population'
                },
                plotLines: [{
                    value: getAverage(values.values),
                    color: 'green',
                    width: 2,
                    label: {
                        text: 'Average = ' + getAverage(values.values)
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
                data: values.values

            }]
        });
    });

    $("button#addMetric").click(function() {

        const core = JSON.parse($(this).attr("data-core"));
        console.log(core);

        const threshold = $("#threshold").val();
        const isBad = $("#high").val();
        const metric = core.source + " | " + core.field;

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
                    'threshold': threshold
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

    var yearNow = moment().year();
    var years = [yearNow];

    for (var x = 0; x < length - 1; x++) {
        yearNow--;
        years.push(yearNow);
    }

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