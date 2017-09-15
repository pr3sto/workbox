/*!
 * new.js
 *
 * js code for box/new.xhtml
 */


$(function ($) {
    // editors
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
            $('#create-button-1').prop('disabled', false);
        else
            $('#create-button-1').prop('disabled', true);
    });

    var templateEditor = CodeMirror.fromTextArea($('#vagrantfile-template-data').get(0), {
        mode: 'text/x-ruby',
        theme: 'neat',
        matchBrackets: true,
        indentUnit: 2,
        lineNumbers: true,
        readOnly: true
    });
    templateEditor.on("change", function(editor, change) {
        if (editor.getValue() !== '')
            $('#create-button-2').prop('disabled', false);
        else
            $('#create-button-2').prop('disabled', true);
    });

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        vagrantfileEditor.refresh();
        templateEditor.refresh();
    });

    // file uploading
    $(':file').on('change', function () {
        $('.loading').css('visibility', 'visible');
        var fr = new FileReader();
        fr.onload = showFile;
        fr.readAsText(this.files[0]);

        function showFile() {
            vagrantfileEditor.setValue(fr.result);
            $('.loading').fadeTo(500, 0, function () {
                $('.loading').css('visibility', 'hidden');
                $('.loading').css('opacity', 1);
            });
        }
    });

    // loading template
    $('select').on('change', function() {
        templateEditor.setValue(this.value);
    });

    // keyboard fix for enter key
    $('.file-label').on('keypress', function(event) {
        if ((event.which || event.keyCode) === 13  ) {
            $('.file-input').click();
            event.preventDefault();
        }
    });
});
