/*!
 * colorsGenerator.js
 *
 * generate colors background
 */


function gen5colorsBackground() {
    var randomColor1 = '#' + Math.random().toString(16).slice(-6);
    var randomColor2 = '#' + Math.random().toString(16).slice(-6);
    var randomColor3 = '#' + Math.random().toString(16).slice(-6);
    var randomColor4 = '#' + Math.random().toString(16).slice(-6);
    var randomColor5 = '#' + Math.random().toString(16).slice(-6);

    return 'white linear-gradient(-90deg,' +
        randomColor1 + ' 20%,' +
        randomColor2 + ' 20%, ' + randomColor2 + ' 40%,' +
        randomColor3 + ' 40%, ' + randomColor3 + ' 60%,' +
        randomColor4 + ' 60%, ' + randomColor4 + ' 80%,' +
        randomColor5 + ' 80%) no-repeat scroll 0px 100% / 100% 2px';
}

function gen10colorsBorder() {
    var randomColor1 = '#' + Math.random().toString(16).slice(-6);
    var randomColor2 = '#' + Math.random().toString(16).slice(-6);
    var randomColor3 = '#' + Math.random().toString(16).slice(-6);
    var randomColor4 = '#' + Math.random().toString(16).slice(-6);
    var randomColor5 = '#' + Math.random().toString(16).slice(-6);
    var randomColor6 = '#' + Math.random().toString(16).slice(-6);
    var randomColor7 = '#' + Math.random().toString(16).slice(-6);
    var randomColor8 = '#' + Math.random().toString(16).slice(-6);
    var randomColor9 = '#' + Math.random().toString(16).slice(-6);
    var randomColor10 = '#' + Math.random().toString(16).slice(-6);

    return 'linear-gradient(-90deg,' +
        randomColor1 + ' 10%,' +
        randomColor2 + ' 10%, ' + randomColor2 + ' 20%,' +
        randomColor3 + ' 20%, ' + randomColor3 + ' 30%,' +
        randomColor4 + ' 30%, ' + randomColor4 + ' 40%,' +
        randomColor5 + ' 40%, ' + randomColor5 + ' 50%,' +
        randomColor6 + ' 50%, ' + randomColor6 + ' 60%,' +
        randomColor7 + ' 60%, ' + randomColor7 + ' 70%,' +
        randomColor8 + ' 70%, ' + randomColor8 + ' 80%,' +
        randomColor9 + ' 80%, ' + randomColor9 + ' 90%,' +
        randomColor10 + ' 90%) 2';
}
