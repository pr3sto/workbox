/*!
 * drawChart.js
 *
 * draw line chart 
 */


function drawChart(ctx, inputData) {
    Chart.defaults.global.animationEasing = 'easeInOutQuad';
    Chart.defaults.global.responsive = true;
    Chart.defaults.global.scaleOverride = true;
    Chart.defaults.global.scaleShowLabels = false;
    Chart.defaults.global.scaleSteps = 10;
    Chart.defaults.global.scaleStepWidth = 10;
    Chart.defaults.global.scaleStartValue = 0;
    Chart.defaults.global.tooltipFillColor = 'rgba(0, 0, 0, 0.8)';
    Chart.defaults.global.tooltipFontColor = '#fff';
    Chart.defaults.global.tooltipCaretSize = 0;
    Chart.defaults.global.maintainAspectRatio = true;

    Chart.defaults.Line.scaleGridLineColor = '#e5e5e5';
    Chart.defaults.Line.scaleLineColor = '#e5e5e5';

    var gradient = ctx.createLinearGradient(0, 0, 0, 450);
    gradient.addColorStop(0, 'rgba(50, 118, 177, 0.5)');
    gradient.addColorStop(0.5, 'rgba(50, 118, 177, 0.25)');
    gradient.addColorStop(1, 'rgba(50, 118, 177, 0)');

    var data = {
        labels: inputData.labels,
        datasets: [{
            fillColor: gradient,
            strokeColor: '#3276b1',
            pointColor: '#fff',
            pointStrokeColor: '#777',
            pointHighlightFill: '#777',
            pointHighlightStroke: '#777',
            data: inputData.data
        }]
    };

    var chart = new Chart(ctx).Line(data);
}
