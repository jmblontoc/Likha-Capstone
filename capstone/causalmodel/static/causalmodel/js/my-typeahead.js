$(function() {

    var json_barangays = $("#hidden-barangays").data("barangays");

    $("input#recipients-input").tagsinput({
        typeahead: {
            source: json_barangays,
            afterSelect: function() {
                this.$element[0].value = '';
            }
        }
    });
});