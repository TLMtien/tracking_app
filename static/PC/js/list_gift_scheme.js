var scheme1 = $('#Scheme-1')
var scheme2 = $('#Scheme-2')
var list_gift_name = $('#list-gift')

scheme1.click(function() {
    $.ajax({
        type: 'POST',
        url: 'list_gift_scheme/',
        headers: {
            "X-CSRFToken": csrf[0].value
        },
        data: 'ok',

        processData: false,
        contentType: false,
        success: function(response) {
            list_gift_name.innerHTML = response.list_gift_1
            console.log(response.list_gift_1)
            var options = {
                series: [{
                    data: response.list_scheme1
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
                    categories: response.list_scheme1_name,
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
            console.log(response)

        },
        error: function(error) {
            console.log(error)
        }
    })
})







var scheme2 = $('#Scheme-2')

scheme2.click(function() {
    $.ajax({
        type: 'POST',
        url: 'list_gift_scheme/',
        headers: {
            "X-CSRFToken": csrf[0].value
        },
        data: 'ok',

        processData: false,
        contentType: false,
        success: function(response) {
            var options = {
                series: [{
                    data: response.list_scheme2
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
                    categories: response.list_scheme2_name,
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
            console.log(response)

        },
        error: function(error) {
            console.log(error)
        }
    })
})