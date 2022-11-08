$(document).ready(function () {
    //Para modificar por jquery a futuro
});

Highcharts.chart('container', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Relación de Tickets'
    },
    xAxis: {
        categories: dates_tickets,
        crosshair: true,
        labels:{ rotation: -35}
    },
    yAxis: {
        title: {
            useHTML: true,
            text: 'Cantidad Tickets'
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y}</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: [{
        name: 'Total',
        data: total_tickets

    }, {
        name: 'Pendientes',
        data: pending_tickets

    },{
        name: 'En curso',
        data: on_course_tickets

    },
    {
        name: 'Resueltos',
        data: done_tickets

    }, {
        name: 'Rechazados',
        data: rejected_tickets

    }]
});