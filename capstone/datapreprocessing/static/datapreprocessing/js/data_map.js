// $(document).ready(function() {
//
//     $("add-data-map").click(function () {
//
//         var root_cause = $("$root-cause-name").val();
//         var metric = $("$existing-metric").val();
//
//         $.ajax({
//             url: window.location.pathname,
//             method: "POST",
//             data: {
//                'root_cause': root_cause,
//                 'metric': metric
//             },
//             success: function (data) {
//                 location.href = "/data-pre_processing/"
//             },
//             error: function (data) {
//                 console.log("whyyyy");
//             }
//         })
//     })
// }