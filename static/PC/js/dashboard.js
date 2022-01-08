const csrf = document.getElementsByName('csrfmiddlewaretoken')

total_array = []
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
        total_array.push((this.value))
    } else {
        array_province = array_province.filter(e => e !== this.value);
        total_array = total_array.filter(e => e !== this.value);
    }
    from_date = []
    to_date = []
    $('[name = "from-date"]').each(function(i) {
        from_date.push($(this).val());
    });
    $('[name = "to-date"]').each(function(i) {
        to_date.push($(this).val());
    });

    console.log(from_date)
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    var fd = new FormData();
    fd.append('array_province', array_province);
    fd.append('from_date', from_date);
    fd.append('to_date', to_date);
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
            outlet_list.innerHTML = response.list_outlet
            list_type_outlet.innerHTML = response.list_type_outlet
            Consumers_charts.innerHTML = response.Consumers_charts
                //volume_performance.innerHTML = response.volume_performance
                //pie_chart.value
            console.log(response.pie_chart)
                //////////////////////////
            var options = {
                series: response.pie_chart,
                chart: {
                    width: 350,
                    type: 'pie',
                },
                // labels: ['Tiger', 'HNK', 'Orther Beer','Orther'],
                colors: ['#198631', '#95b79d', '#1C263F', '#939393'],
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
            $("#chart-share").empty();
            var chart = new ApexCharts(document.querySelector("#chart-share"), options);
            chart.render();
            ///////////////////////////
            var gift_rp = response.gift
            var options = {
                series: [{
                    data: gift_rp
                }],
                chart: {
                    height: 280,
                    type: 'bar',

                },
                colors: ['#198631', '#1C263F', '#727170', '#b5f398', '#c4c4c4', '#49566e'],

                plotOptions: {
                    bar: {
                        columnWidth: '60%',
                        distributed: true,
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
                legend: {
                    show: true
                },
                xaxis: {
                    categories: response.array_gift,
                    labels: {
                        style: {
                            colors: ['#111'],
                            fontSize: '12px',
                        }
                    },
                },
            };
            $("#chart-product").empty();
            var chart = new ApexCharts(document.querySelector("#chart-product"), options);
            chart.render();
            ////////////////////////////
            //top10
            var top10_name = response.top10_name
            var top10_sale = response.top10_sale
            var top10_table = response.top10_table
            console.log(top10_sale)
            var options = {
                series: [{
                    name: '[Brand] Volume',
                    type: 'column',
                    data: top10_sale,
                }, {
                    name: '[Brand] Table Share',
                    type: 'line',
                    data: top10_table,
                }],
                chart: {
                    height: 370,
                    with: 400,
                    type: 'line',
                },
                stroke: {
                    width: [0, 3],
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
                plotOptions: {
                    bar: {
                        borderRadius: 5,
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
            $("#chart-top").empty();
            var chart = new ApexCharts(document.querySelector("#chart-top"), options);
            chart.render();


            ////////////////////

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
            $("#chart-act").empty();
            var chart = new ApexCharts(document.querySelector("#chart-act"), options);

            chart.render();
            //////////////acti
            var activation = response.activation
            var options = {
                series: [{
                    data: [activation, response.total_activation],
                }, ],
                chart: {
                    height: 200,
                    type: 'bar',
                },
                labels: [''],
                colors: ['#198631', '#1C263F'],
                legend: {
                    show: false,
                },
                plotOptions: {
                    bar: {
                        columnWidth: '15%',
                        distributed: true,
                        borderRadius: 5,
                        horizontal: true,
                        dataLabels: {
                            position: 'center', // top, center, bottom
                        },
                    }
                },


                xaxis: {
                    categories: [''],
                    labels: {
                        style: {
                            colors: ['#111'],
                            fontSize: '12px',
                        }
                    },
                },
                dataLabels: {
                    enabled: true,
                    formatter: function(val) {
                        return val;
                    },
                    style: {
                        fontSize: '12px',
                        //colors: ["red"]
                    }
                },

            };
            $("#chart-acti").empty();
            var chart = new ApexCharts(document.querySelector("#chart-acti"), options);
            chart.render();

            var options = {
                series: [{
                    data: [response.actual_volume, response.target_volume],
                }, ],
                chart: {
                    height: 200,
                    type: 'bar',
                },
                labels: [''],
                colors: ['#198631', '#1C263F'],
                legend: {
                    show: false,
                },
                plotOptions: {
                    bar: {

                        distributed: true,
                        borderRadius: 5,
                        horizontal: true,
                        dataLabels: {
                            position: 'center', // top, center, bottom
                        },
                    }
                },


                dataLabels: {
                    position: 'center', // top, center, bottom
                    enabled: true,
                    formatter: function(val) {
                        return val + "/" + val / response.target_volume * 100 + "%";
                    },
                    style: {
                        fontSize: '12px',
                        //colors: ["red"],

                    },

                },
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 300
                        },
                        legend: {
                            show: false
                        },
                    }
                }]
            };
            $("#chart-prog").empty();
            var chart = new ApexCharts(document.querySelector("#chart-prog"), options);
            chart.render();
        },
        error: function(error) {
            console.log(error)
        }
    })

    console.log(array_province)
    console.log(total_array)

})

///////////////////////////////////
array_type = []
var check_type
var type = $('input[name = "type_outlet"]')
    // type.change(function() {

//     var check_type = $(this).prop('checked');
//     if (check_type) {
//         array_type.push((this.value))

//     } else {
//         array_type = array_type.filter(e => e !== this.value);
//     }

//     from_date = []
//     to_date = []
//     $('[name = "from-date"]').each(function(i) {
//         from_date.push($(this).val());
//     });
//     $('[name = "to-date"]').each(function(i) {
//         to_date.push($(this).val());
//     });
//     const csrf = document.getElementsByName('csrfmiddlewaretoken')
//     var fd = new FormData();
//     fd.append('array_type', array_type);
//     fd.append('from_date', from_date);
//     fd.append('to_date', to_date);
//     $.ajax({
//         type: 'POST',
//         url: 'filter_outlet_type/',
//         headers: {
//             "X-CSRFToken": csrf[0].value
//         },
//         data: fd,

//         processData: false,
//         contentType: false,
//         success: function(response) {
//             console.log(response)
//             Consumers_charts.innerHTML = response.Consumers_charts
//                 //volume_performance.innerHTML = response.volume_performance
//                 //pie_chart.value
//             console.log(response.pie_chart)
//                 //////////////////////////
//             var options = {
//                 series: response.pie_chart,
//                 chart: {
//                     width: 350,
//                     type: 'pie',
//                 },
//                 // labels: ['Tiger', 'HNK', 'Orther Beer','Orther'],
//                 colors: ['#198631', '#95b79d', '#1C263F', '#939393'],
//                 responsive: [{
//                     breakpoint: 480,
//                     options: {
//                         chart: {
//                             width: 200
//                         },
//                         legend: {
//                             position: 'bottom'
//                         }
//                     }
//                 }]
//             };
//             $("#chart-share").empty();
//             var chart = new ApexCharts(document.querySelector("#chart-share"), options);
//             chart.render();
//             ///////////////////////////
//             var gift_rp = response.gift
//             var options = {
//                 series: [{
//                     data: gift_rp
//                 }],
//                 chart: {
//                     height: 280,
//                     type: 'bar',

//                 },
//                 colors: ['#198631', '#1C263F', '#727170', '#b5f398', '#c4c4c4', '#49566e'],

//                 plotOptions: {
//                     bar: {
//                         columnWidth: '60%',
//                         distributed: true,
//                         borderRadius: 5,
//                         dataLabels: {
//                             position: 'top', // top, center, bottom
//                         },
//                     }
//                 },

//                 dataLabels: {
//                     enabled: true,
//                     formatter: function(val) {
//                         return val + "%";
//                     },
//                     offsetY: -20,
//                     style: {
//                         fontSize: '12px',
//                         colors: ["#304758"]
//                     }
//                 },
//                 yaxis: {
//                     axisBorder: {
//                         show: false
//                     },
//                     axisTicks: {
//                         show: false,
//                     },
//                     labels: {
//                         show: false,
//                         formatter: function(val) {
//                             return val + "%";
//                         }
//                     }
//                 },
//                 legend: {
//                     show: true
//                 },
//                 xaxis: {
//                     categories: response.array_gift,
//                     labels: {
//                         style: {
//                             colors: ['#111'],
//                             fontSize: '12px',
//                         }
//                     },
//                 },
//             };
//             $("#chart-product").empty();
//             var chart = new ApexCharts(document.querySelector("#chart-product"), options);
//             chart.render();
//             ////////////////////////////
//             //top10
//             var top10_name = response.top10_name
//             var top10_sale = response.top10_sale
//             var top10_table = response.top10_table
//             console.log(top10_sale)
//             var options = {
//                 series: [{
//                     name: '[Brand] Volume',
//                     type: 'column',
//                     data: top10_sale,
//                 }, {
//                     name: '[Brand] Table Share',
//                     type: 'line',
//                     data: top10_table,
//                 }],
//                 chart: {
//                     height: 370,
//                     with: 400,
//                     type: 'line',
//                 },
//                 stroke: {
//                     width: [0, 3],
//                 },
//                 title: {
//                     text: 'Traffic Sources'
//                 },
//                 dataLabels: {
//                     enabled: true,
//                     enabledOnSeries: [1],
//                     style: {
//                         colors: ['#1C263F']
//                     }
//                 },
//                 plotOptions: {
//                     bar: {
//                         borderRadius: 5,
//                     }
//                 },
//                 labels: top10_name,
//                 colors: ['#198631', '#1C263F'],
//                 yaxis: [{
//                     title: {
//                         text: 'Top 10',
//                     },

//                 }, {
//                     opposite: true,
//                     title: {
//                         text: 'Outlet'
//                     }
//                 }]
//             };
//             $("#chart-top").empty();
//             var chart = new ApexCharts(document.querySelector("#chart-top"), options);
//             chart.render();


//             ////////////////////

//             var options = {
//                 chart: {
//                     height: 200,
//                     type: 'bar',
//                 },
//                 series: [{
//                     name: 'ACT',
//                     data: response.Average_brand_volume,
//                 }],
//                 yaxis: {
//                     axisBorder: {
//                         show: false
//                     },
//                     axisTicks: {
//                         show: false,
//                     },
//                     labels: {
//                         show: false,
//                         formatter: function(val) {
//                             return val + "%";
//                         }
//                     }

//                 },
//                 labels: ['Average Brand Volume', 'Average Target Volume'],
//                 colors: ['#198631', '#1C263F']
//             }
//             $("#chart-act").empty();
//             var chart = new ApexCharts(document.querySelector("#chart-act"), options);

//             chart.render();
//             var activation = response.activation
//             var options = {
//                 series: [{
//                     data: [activation, response.total_activation],
//                 }, ],
//                 chart: {
//                     height: 200,
//                     type: 'bar',
//                 },
//                 labels: [''],
//                 colors: ['#198631', '#1C263F'],
//                 legend: {
//                     show: false,
//                 },
//                 plotOptions: {
//                     bar: {
//                         columnWidth: '15%',
//                         distributed: true,
//                         borderRadius: 5,
//                         horizontal: true,
//                         dataLabels: {
//                             position: 'center', // top, center, bottom
//                         },
//                     }
//                 },


//                 xaxis: {
//                     categories: [''],
//                     labels: {
//                         style: {
//                             colors: ['#111'],
//                             fontSize: '12px',
//                         }
//                     },
//                 },
//                 dataLabels: {
//                     enabled: true,
//                     formatter: function(val) {
//                         return val;
//                     },
//                     style: {
//                         fontSize: '12px',
//                         colors: ["red"]
//                     }
//                 },

//             };
//             $("#chart-acti").empty();
//             var chart = new ApexCharts(document.querySelector("#chart-acti"), options);
//             chart.render();

//             var options = {
//                 series: [{
//                     data: [response.actual_volume, response.target_volume],
//                 }, ],
//                 chart: {
//                     height: 200,
//                     type: 'bar',
//                 },
//                 labels: [''],
//                 colors: ['#198631', '#1C263F'],
//                 legend: {
//                     show: false,
//                 },
//                 plotOptions: {
//                     bar: {

//                         distributed: true,
//                         borderRadius: 5,
//                         horizontal: true,
//                         dataLabels: {
//                             position: 'center', // top, center, bottom
//                         },
//                     }
//                 },


//                 dataLabels: {
//                     position: 'center', // top, center, bottom
//                     enabled: true,
//                     formatter: function(val) {
//                         return val + "/" + val / response.target_volume * 100 + "%";
//                     },
//                     style: {
//                         fontSize: '12px',
//                         colors: ["red"],

//                     },

//                 },
//                 responsive: [{
//                     breakpoint: 480,
//                     options: {
//                         chart: {
//                             width: 300
//                         },
//                         legend: {
//                             show: false
//                         },
//                     }
//                 }]
//             };
//             $("#chart-prog").empty();
//             var chart = new ApexCharts(document.querySelector("#chart-prog"), options);
//             chart.render();
//         },
//         error: function(error) {
//             console.log(error)
//         }
//     })
//     console.log(array_type)
//     console.log(total_array)
// })

// ///////////////////////////////////////////////////
// var array = []

// var check = $('input[name = "name_outlet"]')
// var ischeck

// check.change(function() {

//     var ischeck = $(this).prop('checked');
//     if (ischeck) {
//         array.push((this.value))
//     } else {
//         array = array.filter(e => e !== this.value);

//     }
//     from_date = []
//     to_date = []
//     $('[name = "from-date"]').each(function(i) {
//         from_date.push($(this).val());
//     });
//     $('[name = "to-date"]').each(function(i) {
//         to_date.push($(this).val());
//     });
//     const csrf = document.getElementsByName('csrfmiddlewaretoken')
//     var fd = new FormData();
//     fd.append('array', array);
//     fd.append('from_date', from_date);
//     fd.append('to_date', to_date);
//     $.ajax({
//         type: 'POST',
//         url: 'filter_outlet/',
//         headers: {
//             "X-CSRFToken": csrf[0].value
//         },
//         data: fd,

//         processData: false,
//         contentType: false,
//         success: function(response) {
//             console.log(response)
//             Consumers_charts.innerHTML = response.Consumers_charts
//                 //volume_performance.innerHTML = response.volume_performance
//                 //pie_chart.value
//             console.log(response.pie_chart)
//                 //////////////////////////
//             var options = {
//                 series: response.pie_chart,
//                 chart: {
//                     width: 350,
//                     type: 'pie',
//                 },
//                 // labels: ['Tiger', 'HNK', 'Orther Beer','Orther'],
//                 colors: ['#198631', '#95b79d', '#1C263F', '#939393'],
//                 responsive: [{
//                     breakpoint: 480,
//                     options: {
//                         chart: {
//                             width: 200
//                         },
//                         legend: {
//                             position: 'bottom'
//                         }
//                     }
//                 }]
//             };
//             $("#chart-share").empty();
//             var chart = new ApexCharts(document.querySelector("#chart-share"), options);
//             chart.render();
//             ///////////////////////////
//             var gift_rp = response.gift
//             var options = {
//                 series: [{
//                     data: gift_rp
//                 }],
//                 chart: {
//                     height: 280,
//                     type: 'bar',

//                 },
//                 colors: ['#198631', '#1C263F', '#727170', '#b5f398', '#c4c4c4', '#49566e'],

//                 plotOptions: {
//                     bar: {
//                         columnWidth: '60%',
//                         distributed: true,
//                         borderRadius: 5,
//                         dataLabels: {
//                             position: 'top', // top, center, bottom
//                         },
//                     }
//                 },

//                 dataLabels: {
//                     enabled: true,
//                     formatter: function(val) {
//                         return val + "%";
//                     },
//                     offsetY: -20,
//                     style: {
//                         fontSize: '12px',
//                         colors: ["#304758"]
//                     }
//                 },
//                 yaxis: {
//                     axisBorder: {
//                         show: false
//                     },
//                     axisTicks: {
//                         show: false,
//                     },
//                     labels: {
//                         show: false,
//                         formatter: function(val) {
//                             return val + "%";
//                         }
//                     }
//                 },
//                 legend: {
//                     show: true
//                 },
//                 xaxis: {
//                     categories: response.array_gift,
//                     labels: {
//                         style: {
//                             colors: ['#111'],
//                             fontSize: '12px',
//                         }
//                     },
//                 },
//             };
//             console.log(gift_rp)
//             $("#chart-product").empty();
//             var chart = new ApexCharts(document.querySelector("#chart-product"), options);
//             chart.render();
//             ////////////////////////////
//             //top10
//             var top10_name = response.top10_name
//             var top10_sale = response.top10_sale
//             var top10_table = response.top10_table
//             console.log(top10_sale)
//             var options = {
//                 series: [{
//                     name: '[Brand] Volume',
//                     type: 'column',
//                     data: top10_sale,
//                 }, {
//                     name: '[Brand] Table Share',
//                     type: 'line',
//                     data: top10_table,
//                 }],
//                 chart: {
//                     height: 370,
//                     with: 400,
//                     type: 'line',
//                 },
//                 stroke: {
//                     width: [0, 3],
//                 },
//                 title: {
//                     text: 'Traffic Sources'
//                 },
//                 dataLabels: {
//                     enabled: true,
//                     enabledOnSeries: [1],
//                     style: {
//                         colors: ['#1C263F']
//                     }
//                 },
//                 plotOptions: {
//                     bar: {
//                         borderRadius: 5,
//                     }
//                 },
//                 labels: top10_name,
//                 colors: ['#198631', '#1C263F'],
//                 yaxis: [{
//                     title: {
//                         text: 'Top 10',
//                     },

//                 }, {
//                     opposite: true,
//                     title: {
//                         text: 'Outlet'
//                     }
//                 }]
//             };
//             $("#chart-top").empty();
//             var chart = new ApexCharts(document.querySelector("#chart-top"), options);
//             chart.render();


//             ////////////////////

//             var options = {
//                 chart: {
//                     height: 200,
//                     type: 'bar',
//                 },
//                 series: [{
//                     name: 'ACT',
//                     data: response.Average_brand_volume,
//                 }],
//                 yaxis: {
//                     axisBorder: {
//                         show: false
//                     },
//                     axisTicks: {
//                         show: false,
//                     },
//                     labels: {
//                         show: false,
//                         formatter: function(val) {
//                             return val + "%";
//                         }
//                     }

//                 },
//                 labels: ['Average Brand Volume', 'Average Target Volume'],
//                 colors: ['#198631', '#1C263F']
//             }
//             $("#chart-act").empty();
//             var chart = new ApexCharts(document.querySelector("#chart-act"), options);

//             chart.render();
//             var activation = response.activation
//             var options = {
//                 series: [{
//                     data: [activation, response.total_activation],
//                 }, ],
//                 chart: {
//                     height: 200,
//                     type: 'bar',
//                 },
//                 labels: [''],
//                 colors: ['#198631', '#1C263F'],
//                 legend: {
//                     show: false,
//                 },
//                 plotOptions: {
//                     bar: {
//                         columnWidth: '15%',
//                         distributed: true,
//                         borderRadius: 5,
//                         horizontal: true,
//                         dataLabels: {
//                             position: 'center', // top, center, bottom
//                         },
//                     }
//                 },


//                 xaxis: {
//                     categories: [''],
//                     labels: {
//                         style: {
//                             colors: ['#111'],
//                             fontSize: '12px',
//                         }
//                     },
//                 },
//                 dataLabels: {
//                     enabled: true,
//                     formatter: function(val) {
//                         return val;
//                     },
//                     style: {
//                         fontSize: '12px',
//                         colors: ["red"]
//                     }
//                 },

//             };
//             $("#chart-acti").empty();
//             var chart = new ApexCharts(document.querySelector("#chart-acti"), options);
//             chart.render();

//             var options = {
//                 series: [{
//                     data: [response.actual_volume, response.target_volume],
//                 }, ],
//                 chart: {
//                     height: 200,
//                     type: 'bar',
//                 },
//                 labels: [''],
//                 colors: ['#198631', '#1C263F'],
//                 legend: {
//                     show: false,
//                 },
//                 plotOptions: {
//                     bar: {

//                         distributed: true,
//                         borderRadius: 5,
//                         horizontal: true,
//                         dataLabels: {
//                             position: 'center', // top, center, bottom
//                         },
//                     }
//                 },


//                 dataLabels: {
//                     position: 'center', // top, center, bottom
//                     enabled: true,
//                     formatter: function(val) {
//                         return val + "/" + val / response.target_volume * 100 + "%";
//                     },
//                     style: {
//                         fontSize: '12px',
//                         colors: ["red"],

//                     },

//                 },
//                 responsive: [{
//                     breakpoint: 480,
//                     options: {
//                         chart: {
//                             width: 300
//                         },
//                         legend: {
//                             show: false
//                         },
//                     }
//                 }]
//             };
//             $("#chart-prog").empty();
//             var chart = new ApexCharts(document.querySelector("#chart-prog"), options);
//             chart.render();
//         },
//         error: function(error) {
//             console.log(error)
//         }
//     })
//     console.log(array)
// })




////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
array1 = []
$("#list_type_outlet").on("change", "input:checkbox", function() {
    var check_exist = false
    var ischeck = $(this).prop('checked');
    if (ischeck) {
        for (let i = 0; i < total_array.length; i++) {
            if (total_array[i] === this.value) {
                check_exist = true
            }
        }
        if (check_exist == false) {
            array1.push((this.value))
            total_array.push((this.value))
        }


    } else {
        array1 = array1.filter(e => e !== this.value);
        total_array = total_array.filter(e => e !== this.value);
        console.log(this.value)
        console.log(total_array)
    }
    from_date = []
    to_date = []
    $('[name = "from-date"]').each(function(i) {
        from_date.push($(this).val());
    });
    $('[name = "to-date"]').each(function(i) {
        to_date.push($(this).val());
    });
    console.log(total_array)
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    var fd = new FormData();
    fd.append('total_array', total_array);
    fd.append('from_date', from_date);
    fd.append('to_date', to_date);
    $.ajax({
        type: 'POST',
        url: 'filter_outlet_type_province/',
        headers: {
            "X-CSRFToken": csrf[0].value
        },
        data: fd,

        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response)
            outlet_list.innerHTML = response.list_outlet
            Consumers_charts.innerHTML = response.Consumers_charts
                //list_type_outlet.innerHTML = response.list_type_outlet
                //volume_performance.innerHTML = response.volume_performance
                //pie_chart.value
            console.log(response.pie_chart)
                //////////////////////////
            var options = {
                series: response.pie_chart,
                chart: {
                    width: 350,
                    type: 'pie',
                },
                // labels: ['Tiger', 'HNK', 'Orther Beer','Orther'],
                colors: ['#198631', '#95b79d', '#1C263F', '#939393'],
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
            $("#chart-share").empty();
            var chart = new ApexCharts(document.querySelector("#chart-share"), options);
            chart.render();
            ///////////////////////////
            var gift_rp = response.gift
            var options = {
                series: [{
                    data: gift_rp
                }],
                chart: {
                    height: 280,
                    type: 'bar',

                },
                colors: ['#198631', '#1C263F', '#727170', '#b5f398', '#c4c4c4', '#49566e'],

                plotOptions: {
                    bar: {
                        columnWidth: '60%',
                        distributed: true,
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
                legend: {
                    show: true
                },
                xaxis: {
                    categories: response.array_gift,
                    labels: {
                        style: {
                            colors: ['#111'],
                            fontSize: '12px',
                        }
                    },
                },
            };
            console.log(gift_rp)
            $("#chart-product").empty();
            var chart = new ApexCharts(document.querySelector("#chart-product"), options);
            chart.render();
            ////////////////////////////
            //top10
            var top10_name = response.top10_name
            var top10_sale = response.top10_sale
            var top10_table = response.top10_table
            console.log(top10_sale)
            var options = {
                series: [{
                    name: '[Brand] Volume',
                    type: 'column',
                    data: top10_sale,
                }, {
                    name: '[Brand] Table Share',
                    type: 'line',
                    data: top10_table,
                }],
                chart: {
                    height: 370,
                    with: 400,
                    type: 'line',
                },
                stroke: {
                    width: [0, 3],
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
                plotOptions: {
                    bar: {
                        borderRadius: 5,
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
            $("#chart-top").empty();
            var chart = new ApexCharts(document.querySelector("#chart-top"), options);
            chart.render();


            ////////////////////

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
            $("#chart-act").empty();
            var chart = new ApexCharts(document.querySelector("#chart-act"), options);

            chart.render();
            var activation = response.activation
            var options = {
                series: [{
                    data: [activation, response.total_activation],
                }, ],
                chart: {
                    height: 200,
                    type: 'bar',
                },
                labels: [''],
                colors: ['#198631', '#1C263F'],
                legend: {
                    show: false,
                },
                plotOptions: {
                    bar: {
                        columnWidth: '15%',
                        distributed: true,
                        borderRadius: 5,
                        horizontal: true,
                        dataLabels: {
                            position: 'center', // top, center, bottom
                        },
                    }
                },


                xaxis: {
                    categories: [''],
                    labels: {
                        style: {
                            colors: ['#111'],
                            fontSize: '12px',
                        }
                    },
                },
                dataLabels: {
                    enabled: true,
                    formatter: function(val) {
                        return val;
                    },
                    style: {
                        fontSize: '12px',
                        //colors: ["red"]
                    }
                },

            };
            $("#chart-acti").empty();
            var chart = new ApexCharts(document.querySelector("#chart-acti"), options);
            chart.render();

            var options = {
                series: [{
                    data: [response.actual_volume, response.target_volume],
                }, ],
                chart: {
                    height: 200,
                    type: 'bar',
                },
                labels: [''],
                colors: ['#198631', '#1C263F'],
                legend: {
                    show: false,
                },
                plotOptions: {
                    bar: {

                        distributed: true,
                        borderRadius: 5,
                        horizontal: true,
                        dataLabels: {
                            position: 'center', // top, center, bottom
                        },
                    }
                },


                dataLabels: {
                    position: 'center', // top, center, bottom
                    enabled: true,
                    formatter: function(val) {
                        return val + "/" + val / response.target_volume * 100 + "%";
                    },
                    style: {
                        fontSize: '12px',
                        //colors: ["red"],

                    },

                },
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 300
                        },
                        legend: {
                            show: false
                        },
                    }
                }]
            };
            $("#chart-prog").empty();
            var chart = new ApexCharts(document.querySelector("#chart-prog"), options);
            chart.render();
        },
        error: function(error) {
            console.log(error)
        }
    })
    console.log(total_array)
        //alert('ok')


});



/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

$("#list_name_outlet").on("change", "input:checkbox", function() {


    var ischeck = $(this).prop('checked');
    if (ischeck) {
        total_array.push((this.value))
    } else {
        total_array = total_array.filter(e => e !== this.value);
    }
    from_date = []
    to_date = []
    $('[name = "from-date"]').each(function(i) {
        from_date.push($(this).val());
    });
    $('[name = "to-date"]').each(function(i) {
        to_date.push($(this).val());
    });
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
    var fd = new FormData();
    fd.append('total_array', total_array);
    fd.append('from_date', from_date);
    fd.append('to_date', to_date);
    $.ajax({
        type: 'POST',
        url: 'filter_outletName_Province_type/',
        headers: {
            "X-CSRFToken": csrf[0].value
        },
        data: fd,

        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response)
                //outlet_list.innerHTML = response.list_outlet
            Consumers_charts.innerHTML = response.Consumers_charts
                //volume_performance.innerHTML = response.volume_performance
                //pie_chart.value
            console.log(response.pie_chart)
                //////////////////////////
            var options = {
                series: response.pie_chart,
                chart: {
                    width: 350,
                    type: 'pie',
                },
                // labels: ['Tiger', 'HNK', 'Orther Beer','Orther'],
                colors: ['#198631', '#95b79d', '#1C263F', '#939393'],
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
            $("#chart-share").empty();
            var chart = new ApexCharts(document.querySelector("#chart-share"), options);
            chart.render();
            ///////////////////////////
            var gift_rp = response.gift
            var options = {
                series: [{
                    data: gift_rp
                }],
                chart: {
                    height: 280,
                    type: 'bar',

                },
                colors: ['#198631', '#1C263F', '#727170', '#b5f398', '#c4c4c4', '#49566e'],

                plotOptions: {
                    bar: {
                        columnWidth: '60%',
                        distributed: true,
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
                legend: {
                    show: true
                },
                xaxis: {
                    categories: response.array_gift,
                    labels: {
                        style: {
                            colors: ['#111'],
                            fontSize: '12px',
                        }
                    },
                },
            };
            console.log(gift_rp)
            $("#chart-product").empty();
            var chart = new ApexCharts(document.querySelector("#chart-product"), options);
            chart.render();
            ////////////////////////////
            //top10
            var top10_name = response.top10_name
            var top10_sale = response.top10_sale
            var top10_table = response.top10_table
            console.log(top10_sale)
            var options = {
                series: [{
                    name: '[Brand] Volume',
                    type: 'column',
                    data: top10_sale,
                }, {
                    name: '[Brand] Table Share',
                    type: 'line',
                    data: top10_table,
                }],
                chart: {
                    height: 370,
                    with: 400,
                    type: 'line',
                },
                stroke: {
                    width: [0, 3],
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
                plotOptions: {
                    bar: {
                        borderRadius: 5,
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
            $("#chart-top").empty();
            var chart = new ApexCharts(document.querySelector("#chart-top"), options);
            chart.render();


            ////////////////////

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
            $("#chart-act").empty();
            var chart = new ApexCharts(document.querySelector("#chart-act"), options);

            chart.render();
            var activation = response.activation
            var options = {
                series: [{
                    data: [activation, response.total_activation],
                }, ],
                chart: {
                    height: 200,
                    type: 'bar',
                },
                labels: [''],
                colors: ['#198631', '#1C263F'],
                legend: {
                    show: false,
                },
                plotOptions: {
                    bar: {
                        columnWidth: '15%',
                        distributed: true,
                        borderRadius: 5,
                        horizontal: true,
                        dataLabels: {
                            position: 'center', // top, center, bottom
                        },
                    }
                },


                xaxis: {
                    categories: [''],
                    labels: {
                        style: {
                            colors: ['#111'],
                            fontSize: '12px',
                        }
                    },
                },
                dataLabels: {
                    enabled: true,
                    formatter: function(val) {
                        return val;
                    },
                    style: {
                        fontSize: '12px',
                        // colors: ["red"]
                    }
                },

            };
            $("#chart-acti").empty();
            var chart = new ApexCharts(document.querySelector("#chart-acti"), options);
            chart.render();

            var options = {
                series: [{
                    data: [response.actual_volume, response.target_volume],
                }, ],
                chart: {
                    height: 200,
                    type: 'bar',
                },
                labels: [''],
                colors: ['#198631', '#1C263F'],
                legend: {
                    show: false,
                },
                plotOptions: {
                    bar: {

                        distributed: true,
                        borderRadius: 5,
                        horizontal: true,
                        dataLabels: {
                            position: 'center', // top, center, bottom
                        },
                    }
                },


                dataLabels: {
                    position: 'center', // top, center, bottom
                    enabled: true,
                    formatter: function(val) {
                        return val + "/" + val / response.target_volume * 100 + "%";
                    },
                    style: {
                        fontSize: '12px',
                        //colors: ["red"],

                    },

                },
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 300
                        },
                        legend: {
                            show: false
                        },
                    }
                }]
            };
            $("#chart-prog").empty();
            var chart = new ApexCharts(document.querySelector("#chart-prog"), options);
            chart.render();
        },
        error: function(error) {
            console.log(error)
        }
    })
    console.log(total_array)
        //alert('ok')


});