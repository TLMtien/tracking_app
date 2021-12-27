const csrf = document.getElementsByName('csrfmiddlewaretoken')

var array = []

var check = $('input[name = "name_outlet"]')
var ischeck

// check.change(function() {

//     var ischeck = $(this).prop('checked');
//     if (ischeck) {
//         array.push((this.value))
//     } else {
//         array = array.filter(e => e !== this.value);
//     }
//     const csrf = document.getElementsByName('csrfmiddlewaretoken')
//     var fd = new FormData();
//     fd.append('array', array);
//     $.ajax({
//         type: 'POST',
//         url: '{% url "outlet_approval_byHVN" %}',
//         headers: {
//             "X-CSRFToken": csrf[0].value
//         },
//         data: fd,

//         processData: false,
//         contentType: false,
//         success: function(response) {
//             console.log(response)
//         },
//         error: function(error) {
//             console.log(error)
//         }
//     })
//     console.log(array)
// })

///////////////
array_province = []
var province = $('input[name = "province"]')
var checked_pro
outlet_list = document.getElementById('list_name_outlet')
pie_chart = document.getElementById('pie')
list_type_outlet = document.getElementById('list_type_outlet')
Consumers_charts = document.getElementById('Consumers_charts')
volume_performance = document.getElementById('volume_performance')
    ///////////////

province.change(function() {

    var checked_pro = $(this).prop('checked');
    if (checked_pro) {
        array_province.push((this.value))
    } else {
        array_province = array_province.filter(e => e !== this.value);
    }


    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    var fd = new FormData();
    fd.append('array_province', array_province);
    $.ajax({
        type: 'POST',
        url: 'filter-outlet-province/',
        headers: {
            "X-CSRFToken": csrf[0].value
        },
        data: fd,

        processData: false,
        contentType: false,
        success: function(response) {

            console.log(response)
                //outlet_list.innerHTML = response.list_outlet
                //list_type_outlet.innerHTML = response.list_type
            Consumers_charts.innerHTML = response.Consumers_charts
            volume_performance.innerHTML = response.volume_performance
                //pie_chart.value
            console.log(response.pie_chart)
            var options = {
                series: response.pie_chart,
                chart: {
                    width: 350,
                    type: 'pie',
                },
                labels: ['HVN', 'Brand', 'Other', 'Other beer'],
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

            var gift_rp = response.gift
            var options = {
                series: [{
                    name: 'Inflation',
                    data: gift_rp,
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
            //top10
            var top10_name = response.top10_name
            var top10_sale = response.top10_sale
            var top10_table = response.top10_table
            console.log(top10_sale)
            var options = {
                series: [{
                    name: 'Total',
                    type: 'column',
                    data: top10_sale,
                }, {
                    name: 'Top %',
                    type: 'line',
                    data: top10_table,
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

                labels: top10_name,
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

            var options = {
                chart: {
                    height: 200,
                    type: 'bar',
                },
                series: [{
                    name: 'ACT',
                    data: response.Average_brand_volume,
                }],
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
                labels: ['Average Brand Volume', 'Average Target Volume'],
                colors: ['#198631', '#1C263F']
            }

            var chart = new ApexCharts(document.querySelector("#chart-act"), options);

            chart.render();
        },
        error: function(error) {
            console.log(error)
        }
    })
    console.log(array_province)
})

///////////////////////////////////
array_type = []
var check_type
var type = $('input[name = "type_outlet"]')
type.change(function() {

    var check_type = $(this).prop('checked');
    if (check_type) {
        array_type.push((this.value))
    } else {
        array_type = array_type.filter(e => e !== this.value);
    }
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    var fd = new FormData();
    fd.append('array_type', array_type);
    $.ajax({
        type: 'POST',
        url: 'filter-outlet-province/',
        headers: {
            "X-CSRFToken": csrf[0].value
        },
        data: fd,

        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response)
        },
        error: function(error) {
            console.log(error)
        }
    })
    console.log(array_type)

})