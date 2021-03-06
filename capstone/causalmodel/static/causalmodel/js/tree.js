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

    var GO = go.GraphObject.make;
    var diagram = GO(go.Diagram, "tree", { layout: GO(go.TreeLayout, { angle: 90, layerSpacing: 35 }) });
    var myModel = GO(go.TreeModel);

    defaultRootCauses.each(function () {

        var name = $(this).parent().siblings(".rc-name").html();
        var id = $(this).parent().parent().attr('data-id');
        blocks.push(
            new Block(id, name, [], true, null)
        );
    });

    var rootCauseSelect = $("#root-cause-select");

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

        diagram.nodeTemplate =
           GO(go.Node, "Vertical",
               GO(go.Panel, "Vertical", { background: "white", padding: 10 },
                   GO(go.TextBlock, new go.Binding("text", "name"), { font: "bold 12pt Arial" })
               )
           );

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


        kids = [];

        for (s in selected) {

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

        // blocks.push(
        //     new Block(null, "end", [], false,
        //         [blocks[blocks.length - 1]])
        // );

        var sons = [];

        for (b in blocks) {
            if (blocks[b].id == null) {
                var b1 = blocks[b];

                if (b1.child != null) {
                    for (c in b1.child) {

                        sons.push({
                            "key": b1.child[c].name,
                            "name": b1.child[c].name,
                            "parent": b1.name
                        });
                    }
                }
                else {
                    console.log("it went here");

                }
            }
        }
        console.log('end', blocks);
        myModel.nodeDataArray = addDummy(sons);

        diagram.model = myModel;

    });

    $("#createTree").click(function() {

        addedBlocks = [];

        for (b in blocks) {
            addedBlocks.push(blocks[b]);
        }

        var endBlock = new Block(null, 'end', [] , false, [addedBlocks[addedBlocks.length - 1]]);
        addedBlocks.push(endBlock);

        var ajaxReady = JSON.stringify(addedBlocks);
        console.log(addedBlocks);
        $.ajax({
            url: "/causal-models/create_tree",
            type: "post",
            data: {
                'blocks': ajaxReady
            },
            dataType: "json",
            success: function(data) {
                console.log(data);
                alert("Causal model created successfully");

                window.location.replace('/causal-models/' + moment().year());
            },
            error: function(x) {
                console.log(x.responseText);
            }
        });
    });

    function getParents(sons) {

        // get unique instances of parents
        var parents = [];
        for (var s in sons) {
            if (!parents.includes(sons[s].parent)) {
                parents.push(sons[s].parent);
            }
        }

        return parents;
    }

    function getKeys(sons) {
        var keys = [];

        for (var s in sons) {
            keys.push(sons[s].key);
        }

        return keys;
    }

    function addDummy(sons) {

        var dummy = [];
        var parents = getParents(sons);

        for (var parent in parents) {
            if (!getKeys(sons).includes(parents[parent])) {
                dummy.push(parents[parent]);
            }
        }

        for (var d in dummy) {
            sons.push({
                "key": dummy[d],
                "name": dummy[d],
                "parent": ""
            });
        }

        return sons;
    }

    function removeUndefinedSons(sons) {

        for (var x = sons.length - 1; x >= 0; x--) {
            if (typeof(sons[x].parent) === 'undefined') {
                sons.splice(x, 1);
            }
        }
    }

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

    function getEndIndex(arr) {

        var len = arr.length;

        for (var i = len - 1; i >= 0; i--) {

            if (arr[i].name === 'end') {
                return i
            }
        }

        return -1;
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

    this.id = id;
    this.name = name;
    this.rootCauses = rootCauses;
    this.isDefault = isDefault;
    this.child = child;
}

function Relationship() {

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