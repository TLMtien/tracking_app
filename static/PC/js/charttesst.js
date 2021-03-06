// chart-act

var options = {
    chart: {
        type: 'bar'
    },
    series: [{
        name: 'ACT',
        data: [160, 167],
    }],
    labels: ['Total'],
    colors: ['#198631', '#1C263F']
}

var chart = new ApexCharts(document.querySelector("#chart-act"), options);

chart.render();


//   chart-share

var options = {
    series: [150, 35, 10, 1],
    chart: {
        width: 350,
        type: 'pie',
    },
    labels: ['Heineken', 'HNK', 'Other beer', 'other'],
    colors: ['#198631', '#1C263F', '#000', '#939393'],
    responsive: [{
        breakpoint: 480,
        options: {
            chart: {
                width: 200
            },
            legend: {
                position: 'bottom'
            }
        }
    }]
};

var chart = new ApexCharts(document.querySelector("#chart-share"), options);
chart.render();

// chart-product

var options = {
    series: [{
        name: 'Inflation',
        data: [15, 20, 10, 5, 15]
    }],
    chart: {
        height: 270,
        type: 'bar',
    },
    plotOptions: {
        bar: {
            borderRadius: 5,
            dataLabels: {
                position: 'top', // top, center, bottom
            },

        }
    },
    dataLabels: {
        enabled: true,
        formatter: function(val) {
            return val + "%";
        },
        offsetY: -20,
        style: {
            fontSize: '12px',
            colors: ["#304758"]
        }
    },
    yaxis: {
        axisBorder: {
            show: false
        },
        axisTicks: {
            show: false,
        },
        labels: {
            show: false,
            formatter: function(val) {
                return val + "%";
            }
        }

    },
    title: {
        text: 'Total',
        floating: true,
        offsetY: 240,
        align: 'center',
        style: {
            color: '#444'
        }
    },
    labels: [''],
    colors: ['#198631', '#1C263F'],


};

var chart = new ApexCharts(document.querySelector("#chart-product"), options);
chart.render();

// chart-top

var options = {
    series: [{
        name: 'Total',
        type: 'column',
        data: [1152, 1000, 660, 648, 618, 600, 546, 538, 534, 527]
    }, {
        name: 'Top %',
        type: 'line',
        data: [90, 81, 43, 94, 100, 100, 95, 65, 87, 78],
    }],
    chart: {
        height: 350,
        type: 'line',
    },
    stroke: {
        width: [0, 4],
    },
    title: {
        text: 'Traffic Sources'
    },
    dataLabels: {
        enabled: true,
        enabledOnSeries: [1],
        style: {
            colors: ['#1C263F']
        }
    },
    labels: ['H???N', 'L??A N???P', '???C NGON', 'T??', '?????NG N???I', 'TR??NG AN', 'B?? T??', 'H????NG', 'L???U 79', 'L???U D??'],
    colors: ['#198631', '#1C263F'],
    yaxis: [{
        title: {
            text: 'Top 10',
        },

    }, {
        opposite: true,
        title: {
            text: 'Outlet'
        }
    }]
};

var chart = new ApexCharts(document.querySelector("#chart-top"), options);
chart.render();