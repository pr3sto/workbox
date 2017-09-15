/*!
 * list.js
 *
 * js code for box/list.xhtml
 */


$(function ($) {
    // box table
    var boxTable = $('#box-table').dataTable({
        fixedHeader: {
            header: true,
            headerOffset: 50
        },
        pagingType: "numbers",
        language: {
            url: "/local/datatables.ru.lang"
        },
        ajax: "/box/get",
        columnDefs: [{ 
            'targets': -1,
            'render': function (data, type, full, meta) {
                row_html = '';
                if (full[2] != 'started') {
                    row_html += '<button data-toggle="confirmation" name="start_box" value="' +
                     full[0] + '" class="btn btn-success">Запустить</button>';
                } else if (full[2] == 'started') {
                    row_html += '<button data-toggle="confirmation" name="stop_box" value="' 
                    + full[0] + '" class="btn btn-warning">Остановить</button>'
                }
                row_html += '<button data-toggle="confirmation" name="copy_box" value="' 
                + full[0] + '" class="btn btn-default">Копировать</button>'
                row_html += '<button data-toggle="confirmation" name="delete_box" value="' 
                + full[0] + '" class="btn btn-danger" style="width:auto;"><span class="glyphicon glyphicon-trash"/></button>'
                return row_html;
            },
            'orderable': false
        }],
        fnDrawCallback: function(settings, json) {
            $('#box-table tbody button').click(function(e) {
                e.stopPropagation();
            });
            $('[data-toggle="confirmation"]').confirmation({
                rootSelector: '[data-toggle=confirmation]',
                copyAttributes: 'name value',
                singleton:true,
                popout:true,
                placement:'left',
                title:'Вы уверены?',
                btnOkClass:'btn-primary',
                btnCancelClass:'btn-default',
                btnOkLabel:'',
                btnCancelLabel:'',
                onConfirm: function() {
                    window[$(this).attr('name')]($(this).attr('value'));
                }
            });
        }
    });
    $('#box-table tbody').on( 'click', 'tr', function () {
        window.location.href = '/box/id/' + boxTable.fnGetData(this)[0];
    });
});

// actions
function action_call_ajax(url, notification) {
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
            var boxTable = $('#box-table').dataTable();
            boxTable.api().ajax.reload(null, false);
            $.notify({
                title: '<b>WorkBox:</b>',
                message: notification
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
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            document.write(XMLHttpRequest.responseText);
        }
    });
}
function start_box(value) {
    action_call_ajax('/box/start/' + value, 'Виртуальная среда успешно запущена');
}
function stop_box(value) {
    action_call_ajax('/box/stop/' + value, 'Виртуальная среда успешно остановлена');
}
function copy_box(value) {
    action_call_ajax('/box/copy/' + value, 'Виртуальная среда успешно скопирована');
}
function delete_box(value) {
    action_call_ajax('/box/delete/' + value, 'Виртуальная среда успешно удалена');
}
function update_status() {
    $.ajax({
        type: 'POST',
        url: '/box/update_status',
        beforeSend: function(data) {
            $('#update_status_button').prop('disabled', true);
        },
        success: function(response){ 
            $.notify({
                title: '<b>WorkBox:</b>',
                message: 'Статус обновлен. Закройте это уведомление для обновления таблицы'
            },{
                type: 'info',
                newest_on_top: 'true',
                element: 'body',
                placement: {
                    from: 'bottom',
                    align: 'right'
                },
                delay: '0',
                z_index: '999999',
                animate: {
                    enter: 'animated fadeInDown',
                    exit: 'animated fadeOutDown'
                },
                onClose: function () {
                    var boxTable = $('#box-table').dataTable();
                    boxTable.api().ajax.reload(null, false);
                    $('#update_status_button').prop('disabled', false);
                }
            });
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            document.write(XMLHttpRequest.responseText);
        }
    });
    return false;
}    
