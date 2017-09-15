/*!
 * history.js
 *
 * js code for history.xhtml
 */


$(function ($) {
    // table
    $('#history-table').dataTable({
        fixedHeader: {
            header: true,
            headerOffset: 50
        },
        pagingType: 'numbers',
        language: {
            url: '/local/datatables.ru.lang'
        },
        columnDefs: [{ 
            'targets': -3,
            'render': function (data, type, full, meta) { 
                if (data == ' - ') {
                    return data;
                } else {
                    return "<a href='/box/id/" + data + "'>#" + data + "<a>";
                }
            }
        }],
        ajax: '/history/get'
    });
});
