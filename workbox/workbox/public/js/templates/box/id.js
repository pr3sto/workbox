/*!
 * id.js
 *
 * js code for box/id.xhtml
 */


$(function ($) {
    // confirmation buttons
    $('[data-toggle="confirmation"]').confirmation({
        rootSelector: '[data-toggle=confirmation]',
        copyAttributes: 'name value',
        singleton: true,
        popout: true,
        placement: 'left',
        title: 'Вы уверены?',
        btnOkClass: 'btn-primary',
        btnCancelClass: 'btn-default',
        btnOkLabel: '',
        btnCancelLabel: '',
        onConfirm: function() {
            window[$(this).attr('name')]($(this).attr('value'));
        }
    });

    // code editor
    var vagrantfileEditor = CodeMirror.fromTextArea($('#vagrantfile-data').get(0), {
        mode: 'text/x-ruby',
        theme: 'neat',
        matchBrackets: true,
        indentUnit: 2,
        lineNumbers: true,
        styleActiveLine: true
    });
    vagrantfileEditor.on("change", function(editor, change) {
        if (editor.getValue() !== '')
            $('#update-button').css('visibility', 'visible');
        else
            $('#update-button').css('visibility', 'hidden');
    });

    // vagrant editor update button
    $("#update_vagrantfile").submit(function() {
        var form = $(this);
        var data = form.serialize();
        $.ajax({
            type: 'POST',
            url: '/box/update_vagrantfile/',
            data: data,
            beforeSend: function(data) {
                $('.loading').css('visibility', 'visible');
            },
            success: function(response){ 
                vagrantfileEditor.setValue(response);
                $('#update-button').css('visibility', 'hidden');
                $('.loading').fadeTo(500, 0, function () {
                    $('.loading').css('visibility', 'hidden');
                    $('.loading').css('opacity', 1);
                });
                $.notify({
                    title: '<b>WorkBox:</b>',
                    message: 'Vagrantfile успешно обновлен'
                },{
                    type: 'success',
                    newest_on_top: 'true',
                    element: 'body',
                    placement: {
                        from: 'bottom',
                        align: 'right'
                    },
                    mouse_over: 'pause',
                    z_index: '999999',
                    animate: {
                        enter: 'animated fadeInDown',
                        exit: 'animated fadeOutDown'
                    }
                });
            },
            error: function(request, error) {
                if (request.responseText != undefined) {
                    document.open();
                    document.write(request.responseText);
                    document.close();
                }
            }
        });
        return false;
    });
});

// actions

function start_box(value) {
    action_call_ajax('/box/start/' + value, function() {
        location.reload();
    });
}

function stop_box(value) {
    action_call_ajax('/box/stop/' + value, function() {
        location.reload();
    });
}

function copy_box(value) {
    action_call_ajax('/box/copy/' + value, function() {
        $.notify({
            title: '<b>WorkBox:</b>',
            message: 'Виртуальная среда успешно скопирована'
        },{
            type: 'success',
            newest_on_top: 'true',
            element: 'body',
            placement: {
                from: 'bottom',
                align: 'right'
            },
            mouse_over: 'pause',
            z_index: '999999',
            animate: {
                enter: 'animated fadeInDown',
                exit: 'animated fadeOutDown'
            }
        });
    });
}

function delete_box(value) {
    action_call_ajax('/box/delete/' + value, function() { 
        window.location.href = '/box/list/';
    });
}

function action_call_ajax(url, action) {
    $.ajax({
        type: 'POST',
        url: url,
        beforeSend: function(data) {
            $('.loading').css('visibility', 'visible');
        },
        success: function(response){ 
            $('.loading').fadeTo(500, 0, function () {
                $('.loading').css('visibility', 'hidden');
                $('.loading').css('opacity', 1);
            });
            action();
        },
        error: function(request, error) {
            if (request.responseText != undefined) {
                document.open();
                document.write(request.responseText);
                document.close();
            }
        }
    });
    return false;
}
