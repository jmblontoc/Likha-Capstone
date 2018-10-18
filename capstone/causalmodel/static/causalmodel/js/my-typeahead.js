$(function() {

    var json_barangays = $("#hidden-barangays").data("barangays");

    var data = json_barangays;

    var citynames = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local: $.map(data, function (city) {
            return {
                name: city
            };
        })
    });
    citynames.initialize();


    $('input#recipients-input').tagsinput({
        typeaheadjs: [{
              minLength: 1,
              highlight: true,
        },{
            minlength: 1,
            name: 'citynames',
            displayKey: 'name',
            valueKey: 'name',
            source: citynames.ttAdapter()
        }],
            freeInput: true
    });
});