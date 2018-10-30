$(function() {

    const modal = $("#intervention-modal");
    const saveBtn = $(".save");

    var html = "<div class='m-2'>" +
                "<input class='form-control intervention-input' placeholder='Enter intervention'>" +
                "</div>";

    modal.on('show.bs.modal', function(e) {

        const button = $(e.relatedTarget);
        const thisModal = $(this);

        const id = button.data("id");
        const content = thisModal.find('.modal-body');
        content.data("id", id);

        content.empty();

        $.ajax({
            url: "/conf/get_interventions",
            type: "GET",
            data: {
                "metric": id
            },
            success: function(data) {

                if (data === '') {
                    content.append(html);
                }
                else {

                }
            },
            error: function(e) {
                console.log(e.responseText);
            }
        });
    });

    $(".add-intervention").click(function() {

        var body = $(this).parent().siblings(".modal-body");

        body.append(html);
    });

    saveBtn.click(function() {
        save(
            $(this).parent().siblings(".modal-body").data("id")
        )

        alert("Interventions successfully set");
        window.location.reload();
    });

    function save(id) {

        var interventions = $(".intervention-input");
        var arr = [];

        interventions.each(function() {
            arr.push($(this).val());
        });

        var jsond = JSON.stringify(arr);

        $.ajax({
            url: "/conf/ajax_set_interventions",
            data: {
                "metric": id,
                "interventions": jsond
            },
            type: "GET",
            success: function() {
                console.log("It happened");
            },
            error: function(e) {
                console.log(e.responseText);
            }
        });
    }
});