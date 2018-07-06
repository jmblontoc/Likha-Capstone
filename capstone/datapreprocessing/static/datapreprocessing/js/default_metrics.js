$(function() {
    // console.log("test");

    $("#viewDefault").on("show.bs.modal", function(e) {

        const button = $(e.relatedTarget);
        const report = button.data('report');
        const table = $("#metric-table");

        $.ajax({
            url: "/data-pre_processing/default/ajax",
            type: "get",
            dataType: "json",
            data: {
                'report': report
            },
            success: function(d) {

                table.empty();

                for (var x in d) {
                    table.append('<tr>' +
                        '<td class="text-danger"><i class="fa fa-exclamation-circle"></i>'+ d[x].field +'</td>' +
                        '<td class="text-right">'+ d[x].threshold +'</td>' +
                        '<td class="text-right">'+ d[x].value +'</td>' +
                        '</tr>');
                }
            },
            error: function(e) {
                console.log(e.responseText);
            }
        })
    });
});