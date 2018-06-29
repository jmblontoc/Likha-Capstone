$(function() {

    const modal = $("#causalModelForm");
    const body = $('.form-body');
    const head = $(".form-head");
    const msg = $(".empty");
    const choices = $(".table-body");
    const submit = $("#generateCM");
    const otherBlocks = $(".added-blocks-table");
    const otherBlocksBody = $(".other-blocks");
    const blockName = $("#block-name");
    var selected;
    var rcModalArr;

    var blocks = [];

    var defaultRootCauses = $("input.blocks");

    defaultRootCauses.each(function () {

        var name = $(this).parent().siblings(".rc-name").html();
        var id = $(this).parent().parent().attr('data-id');
        blocks.push(
            new Block(id, name, [], true, null)
        );
    });


    modal.on('shown.bs.modal', function(){

        selected = [];

        $('input.blocks:checked').each(function() {

            var box = $(this);

            var id = box.parent().parent().attr('data-id');
            var name = box.parent().siblings('.rc-name').html();

            selected.push({
                'id': id,
                'name': name
            });

        });

        if (selected.length === 0) {
            head.hide();
            msg.show();
            submit.hide();
        }
        else {
            msg.hide();
            head.show();
            choices.empty();
            submit.show();

            var html = '';

            if (has_undefined(selected)) {
                var title = '<tr><td colspan="2">Add a root cause </td></tr> ';
                choices.append(title);

                for (b in blocks) {

                    if (blocks[b].isDefault) {

                        var row = '<tr>><td class="rc-name">' + blocks[b].name + '</td>' +
                            '<td style="display: none;" class="rc-id">' + blocks[b].id + '</td>' +
                            '<td><input type="checkbox" class="modal-blocks"></td></tr>';
                        choices.append(row);
                    }
                }
            }

            for (x in selected) {

                if (typeof selected[x].id === 'undefined') {

                }

                else {
                     html += '' +
                        '<tr>' +
                        '<td>' + selected[x].name + '</td>' +
                        '</tr>';
                }

            }

            choices.append(html);
        }
    });

    submit.click(function() {

        rcModalArr = [];

        var modalArr = $('.modal-blocks:checked');

        modalArr.each(function() {

            var id =$(this).parent().siblings('.rc-id').html();
            var name = $(this).parent().siblings('.rc-name').html();

            rcModalArr.push({
                'id': id,
                'name': name
            });

        });

        console.log(selected);

        kids = [];

        for (s in selected) {

            console.log(selected[s]);

            kids.push(
                getBlock(selected[s].name)
            );
        }

        blocks.push(
            new Block(null, blockName.val(), rcModalArr, false, kids)
        );


        $('input.blocks').each(function(){
            $(this).prop('checked', false);
        });


        modal.modal('hide');

        otherBlocks.show();

        var html = '<tr>' +
            '<td class="rc-name">' + blockName.val() + '</td>' +
            '<td><input type="checkbox" class="blocks"></td> ' +
            '</tr>';

        blockName.val('');

        otherBlocksBody.append(html);

        console.log(blocks);
    });

    function has_undefined(arr) {

        for (x in arr) {
            if (typeof arr[x].id === 'undefined')
                return true;
        }

        return false;
    }

    function removeUndefined(arr) {

        for (x in arr) {
            if (typeof arr[x].id === 'undefined')
                arr.splice(x, 1);
        }
    }

    function getBlock(name) {

        for (block in blocks) {
            if (blocks[block].name === name) {
                return blocks[block];
            }
        }

        return null;
    }

});

function Block(id, name, rootCauses, isDefault, child) {

    this.name = name;
    this.rootCauses = rootCauses;
    this.isDefault = isDefault;
    this.child = child;
    this.id = id;

}

function Relationship() {

}