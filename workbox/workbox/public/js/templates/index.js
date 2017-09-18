/*!
 * index.js
 *
 * js code for index.xhtml
 */


$(function ($) {
    action_call_ajax('/get_load_value', function(response) {
        $('#doughnutGauge').drawDoughnutGauge(response); 
    });
    
    action_call_ajax('/get_number_of_user_boxes', function(response) {
        var boxes = JSON.parse(response); 
        $('#doughnutChart1').drawDoughnutChart([
            { title: "Запущенные", value: boxes.started, color: "#00C853" },
            { title: "Остановленные", value: boxes.stopped, color: "#f44336" },
            { title: "Созданные", value: boxes.created, color: "#00BCD4" }
        ]);
    });

    action_call_ajax('/get_number_of_all_boxes', function(response) {
        var boxes = JSON.parse(response); 
        $('#doughnutChart2').drawDoughnutChart([
            { title: "Запущенные", value: boxes.started, color: "#00C853" },
            { title: "Остановленные", value: boxes.stopped, color: "#f44336" },
            { title: "Созданные", value: boxes.created, color: "#00BCD4" }
        ]);
    });

    action_call_ajax('/box/get_last_ten_worked', function(response) {
        var boxes = JSON.parse(response); 
        $.each(boxes, function(i, item) {
            var $tr = $('<tr>').append(
                $('<td>').html("<a href='/box/id/" + item.box_id + "'>#" + item.box_id + " - " + item.name + " (" + item.status + ")"),
                $('<td>').html('Дата создания: ' + item.datetime_of_creation),
                $('<td>').html('Дата последнего изменения: ' + item.datetime_of_modify)
            ).appendTo('#last-ten-worked-table');
        });
    });
});

function action_call_ajax(url, action) {
    $.ajax({
        type: 'GET',
        url: url,
        success: function(response){ 
            action(response);
        },
        error: function(request, error) {
            if (request.responseText != undefined) {
                document.open();
                document.write(request.responseText);
                document.close();
            }
        }
    });
}
