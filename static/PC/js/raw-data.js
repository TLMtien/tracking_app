$(document).on('click', '#volume-sale', function() {
    var array_report_sale = [];
    var array_brand = [];
    var array_HVN = [];
    var array_compertion = [];
    var array_date = [];
    var array_sale_id = [];

    $('input[name = "brand-volume"]').each(function(i) {
        console.log(this.value);
        array_brand.push($(this).val());
    });
    $('input[name = "HVN-volume"]').each(function(i) {
        console.log(this.value);
        array_HVN.push($(this).val());
    });
    $('input[name = "compertion-volume"]').each(function(i) {
        console.log(this.value);
        array_compertion.push($(this).val());
    });
    $('input[name = "date"]').each(function(i) {
        console.log(this.value);
        array_date.push($(this).val());
    });
    $('input[name = "sale_id"]').each(function(i) {
        console.log(this.value);
        array_sale_id.push($(this).val());
    });
    array_report_sale.push(array_sale_id);
    array_report_sale.push(array_date);
    array_report_sale.push(array_brand);
    array_report_sale.push(array_HVN);
    array_report_sale.push(array_compertion);
    console.log(array_report_sale)
    const csrf = document.getElementsByName('csrfmiddlewaretoken');
    //const csrf = document.getElementsByName('csrfmiddlewaretoken')
    $.ajax({
        type: 'POST',
        url: 'edit_volume_sale/',
        headers: {
            "X-CSRFToken": csrf[0].value
        },
        data: JSON.stringify({ "array_report_sale": array_report_sale }),

        processData: false,
        contentType: false,
        contentType: 'application/json',
        dataType: "json",
        success: function(resp) {
            alert("Đã sửa thành công!!!")
                // if (array_report_sale[2][0] != '') {
                //     document.querySelector('input[name="brand-volume"]').value = array_report_sale[2][0];
                // }
        },
        error: function(error) {
            console.log(error)
        }
    }); // end ajax
}); // end click volume sale

///////////////////////////////////////////////////////////////////
$(document).on('click', '#table-sale', function() {
    var array_report_sale = [];
    var array_brand = [];
    var array_HVN = [];
    var array_beer_other = [];
    var array_other_table = [];
    var array_table_id = [];

    $('input[name = "brand-table"]').each(function(i) {
        //console.log(this.value);
        array_brand.push($(this).val());
    });
    $('input[name = "HVN-table"]').each(function(i) {
        //console.log(this.value);
        array_HVN.push($(this).val());
    });
    $('input[name = "other-beer-table"]').each(function(i) {
        // console.log(this.value);
        array_beer_other.push($(this).val());
    });
    $('input[name = "other-table"]').each(function(i) {
        //console.log(this.value);
        array_other_table.push($(this).val());
    });
    $('input[name = "table_id"]').each(function(i) {
        console.log(this.value);
        array_table_id.push($(this).val());
    });
    array_report_sale.push(array_table_id);
    array_report_sale.push(array_brand);
    array_report_sale.push(array_HVN);
    array_report_sale.push(array_beer_other);
    array_report_sale.push(array_other_table);
    console.log(array_report_sale)
    const csrf = document.getElementsByName('csrfmiddlewaretoken');
    //const csrf = document.getElementsByName('csrfmiddlewaretoken')
    $.ajax({
        type: 'POST',
        url: 'edit_table_sale/',
        headers: {
            "X-CSRFToken": csrf[0].value
        },
        data: JSON.stringify({ "array_report_sale": array_report_sale }),

        processData: false,
        contentType: false,
        contentType: 'application/json',
        dataType: "json",
        success: function(resp) {
            alert("Đã sửa thành công!!!")
            for (let i = 0; i < resp.id.length; i++) {

                $("#total-table" + resp.id[i]).val(resp.list_total_table[i])
                $("#table-share" + resp.id[i]).val(resp.list_percent_table_share[i])
            }

        },
        error: function(error) {
            console.log(error)
        }
    }); // end ajax
}); // end click table sale

//consumer

$(document).on('click', '#consumer', function() {
    var array_report_sale = [];
    var array_total_consumers = [];
    var array_consumers_approached = [];
    var array_consumers_bought = [];
    var array_consumer_id = [];
    $('input[name = "total-consumers"]').each(function(i) {
        //console.log(this.value);
        array_total_consumers.push($(this).val());
    });
    $('input[name = "consumers-approached"]').each(function(i) {
        //console.log(this.value);
        array_consumers_approached.push($(this).val());
    });
    $('input[name = "consumers-bought"]').each(function(i) {
        // console.log(this.value);
        array_consumers_bought.push($(this).val());
    });
    $('input[name = "consumers_id"]').each(function(i) {
        //console.log(this.value);
        array_consumer_id.push($(this).val());
    });
    array_report_sale.push(array_consumer_id);
    array_report_sale.push(array_total_consumers);
    array_report_sale.push(array_consumers_approached);
    array_report_sale.push(array_consumers_bought);
    console.log(array_report_sale)
    const csrf = document.getElementsByName('csrfmiddlewaretoken');
    //const csrf = document.getElementsByName('csrfmiddlewaretoken')
    $.ajax({
        type: 'POST',
        url: 'edit_consumer_rp/',
        headers: {
            "X-CSRFToken": csrf[0].value
        },
        data: JSON.stringify({ "array_report_sale": array_report_sale }),

        processData: false,
        contentType: false,
        contentType: 'application/json',
        dataType: "json",
        success: function(resp) {
            alert("Đã sửa thành công!!!")
                //document.querySelector('input[name="percent-consumers-reach"]').value = resp.consumers_reach;
                //$("#percent-consumers-reach" + resp.id).val(resp.consumers_reach)
                // document.querySelector('input[name="conversion"]').value = resp.conversion;
                //$("#conversion" + resp.id).val(resp.conversion)

            for (let i = 0; i < resp.id.length; i++) {
                $("#percent-consumers-reach" + resp.id[i]).val(resp.list_consumers_reach[i])
                $("#conversion" + resp.id[i]).val(resp.list_conversion[i])
            }
        },
        error: function(error) {
            console.log(error)
        }
    }); // end ajax
}); // end click consumer


/////////////////////////////////////////////////////////////////////////////////
//Gift

$(document).on('click', '#gift', function() {
    //gift receive
    var array_report_sale = [];
    var array_gift_id = [];
    var array_gift_receive_1 = [];
    var array_gift_receive_2 = [];
    var array_gift_receive_3 = [];
    var array_gift_receive_4 = [];
    var array_gift_receive_5 = [];
    var array_gift_receive_6 = [];
    var array_gift_receive_7 = [];
    //gift given
    var array_gift_given_1 = [];
    var array_gift_given_2 = [];
    var array_gift_given_3 = [];
    var array_gift_given_4 = [];
    var array_gift_given_5 = [];
    var array_gift_given_6 = [];
    var array_gift_given_7 = [];
    $('input[name = "gift_id"]').each(function(i) {
        array_gift_id.push($(this).val());
    });
    //gift received
    $('input[name = "gift-receive-1"]').each(function(i) {
        array_gift_receive_1.push($(this).val());
    });
    $('input[name = "gift-receive-2"]').each(function(i) {
        array_gift_receive_2.push($(this).val());
    });
    $('input[name = "gift-receive-3"]').each(function(i) {
        array_gift_receive_3.push($(this).val());
    });
    $('input[name = "gift-receive-4"]').each(function(i) {
        array_gift_receive_4.push($(this).val());
    });
    $('input[name = "gift-receive-5"]').each(function(i) {
        array_gift_receive_5.push($(this).val());
    });
    $('input[name = "gift-receive-6"]').each(function(i) {
        array_gift_receive_6.push($(this).val());
    });
    $('input[name = "gift-receive-7"]').each(function(i) {
        array_gift_receive_7.push($(this).val());

    });

    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_receive_7.length) {
            array_gift_receive_7.push('0');
        }
    }
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_receive_6.length) {
            array_gift_receive_6.push('0');
        }
    }
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_receive_5.length) {
            array_gift_receive_5.push('0');
        }
    }
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_receive_4.length) {
            array_gift_receive_4.push('0');
        }
    }
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_receive_3.length) {
            array_gift_receive_3.push('0');
        }
    }
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_receive_2.length) {
            array_gift_receive_2.push('0');
        }
    }
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_receive_1.length) {
            array_gift_receive_1.push('0');
        }
    }
    //Gift given
    $('input[name = "gift-given-1"]').each(function(i) {
        array_gift_given_1.push($(this).val());
    });
    $('input[name = "gift-given-2"]').each(function(i) {
        array_gift_given_2.push($(this).val());
    });
    $('input[name = "gift-given-3"]').each(function(i) {
        array_gift_given_3.push($(this).val());
    });
    $('input[name = "gift-given-4"]').each(function(i) {
        array_gift_given_4.push($(this).val());
    });
    $('input[name = "gift-given-5"]').each(function(i) {
        array_gift_given_5.push($(this).val());
    });
    $('input[name = "gift-given-6"]').each(function(i) {
        array_gift_given_6.push($(this).val());
    });
    $('input[name = "gift-given-7"]').each(function(i) {
        array_gift_given_7.push($(this).val());

    });
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_given_7.length) {
            array_gift_given_7.push('0');
        }
    }
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_given_6.length) {
            array_gift_given_6.push('0');
        }
    }
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_given_5.length) {
            array_gift_given_5.push('0');
        }
    }
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_given_4.length) {
            array_gift_given_4.push('0');
        }
    }
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_given_3.length) {
            array_gift_given_3.push('0');
        }
    }
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_given_2.length) {
            array_gift_given_2.push('0');
        }
    }
    for (let i = 0; i < array_gift_id.length; i++) {
        if (array_gift_id.length > array_gift_given_1.length) {
            array_gift_given_1.push('0');
        }
    }

    /////////////////

    array_report_sale.push(array_gift_id);
    //array gift receive

    array_report_sale.push(array_gift_receive_1);
    array_report_sale.push(array_gift_receive_2);
    array_report_sale.push(array_gift_receive_3);
    array_report_sale.push(array_gift_receive_4);
    array_report_sale.push(array_gift_receive_5);
    array_report_sale.push(array_gift_receive_6);
    array_report_sale.push(array_gift_receive_7);
    //array gift given
    array_report_sale.push(array_gift_given_1);
    array_report_sale.push(array_gift_given_2);
    array_report_sale.push(array_gift_given_3);
    array_report_sale.push(array_gift_given_4);
    array_report_sale.push(array_gift_given_5);
    array_report_sale.push(array_gift_given_6);
    array_report_sale.push(array_gift_given_7);

    console.log(array_report_sale)
    const csrf = document.getElementsByName('csrfmiddlewaretoken');
    //const csrf = document.getElementsByName('csrfmiddlewaretoken')
    $.ajax({
        type: 'POST',
        url: 'edit_gift_rp/',
        headers: {
            "X-CSRFToken": csrf[0].value
        },
        data: JSON.stringify({ "array_report_sale": array_report_sale }),

        processData: false,
        contentType: false,
        contentType: 'application/json',
        dataType: "json",
        success: function(resp) {
            alert("Đã sửa thành công!!!")
            for (let i = 0; i < resp.id.length; i++) {
                $("#gift-remain1" + resp.id[i]).val(resp.list_gift_remain[i][0])
                $("#gift-remain2" + resp.id[i]).val(resp.list_gift_remain[i][1])
                $("#gift-remain3" + resp.id[i]).val(resp.list_gift_remain[i][2])
                $("#gift-remain4" + resp.id[i]).val(resp.list_gift_remain[i][3])
                $("#gift-remain5" + resp.id[i]).val(resp.list_gift_remain[i][4])
                $("#gift-remain6" + resp.id[i]).val(resp.list_gift_remain[i][5])
                    // $("#gift-remain7" + resp.id[i]).val(resp.list_gift_remain[i][6])
            }
        },
        error: function(error) {
            console.log(error)
        }
    }); // end ajax
});



$(document).on('click', '#gift-scheme1', function() {
    //gift receive
    var array_report_sale = [];
    var array_gift_id = [];
    var array_gift_receive_1 = [];
    var array_gift_receive_2 = [];
    var array_gift_receive_3 = [];
    var array_gift_receive_4 = [];
    var array_gift_receive_5 = [];
    var array_gift_receive_6 = [];
    var array_gift_receive_7 = [];
    //gift given
    var array_gift_given_1 = [];
    var array_gift_given_2 = [];
    var array_gift_given_3 = [];
    var array_gift_given_4 = [];
    var array_gift_given_5 = [];
    var array_gift_given_6 = [];
    var array_gift_given_7 = [];
    //gift received
    $('input[name = "gift-receive-1-scheme2"]').each(function(i) {
        array_gift_receive_1.push($(this).val());
    });
    $('input[name = "gift-receive-2-scheme2"]').each(function(i) {
        array_gift_receive_2.push($(this).val());
    });
    $('input[name = "gift-receive-3-scheme2"]').each(function(i) {
        array_gift_receive_3.push($(this).val());
    });
    $('input[name = "gift-receive-4-scheme2"]').each(function(i) {
        array_gift_receive_4.push($(this).val());
    });
    $('input[name = "gift-receive-5-scheme2"]').each(function(i) {
        array_gift_receive_5.push($(this).val());
    });
    $('input[name = "gift-receive-6-scheme2"]').each(function(i) {
        array_gift_receive_6.push($(this).val());
    });
    $('input[name = "gift-receive-7-scheme2"]').each(function(i) {
        array_gift_receive_7.push($(this).val());

    });

    for (let i = 0; i < array_gift_receive_1.length; i++) {
        if (array_gift_receive_1.length > array_gift_receive_7.length) {
            array_gift_receive_7.push('0');
        }
    }
    //Gift given
    $('input[name = "gift-given-1-scheme2"]').each(function(i) {
        array_gift_given_1.push($(this).val());
    });
    $('input[name = "gift-given-2-scheme2"]').each(function(i) {
        array_gift_given_2.push($(this).val());
    });
    $('input[name = "gift-given-3-scheme2"]').each(function(i) {
        array_gift_given_3.push($(this).val());
    });
    $('input[name = "gift-given-4-scheme2"]').each(function(i) {
        array_gift_given_4.push($(this).val());
    });
    $('input[name = "gift-given-5-scheme2"]').each(function(i) {
        array_gift_given_5.push($(this).val());
    });
    $('input[name = "gift-given-6-scheme2"]').each(function(i) {
        array_gift_given_6.push($(this).val());
    });
    $('input[name = "gift-given-7-scheme2"]').each(function(i) {
        array_gift_given_7.push($(this).val());

    });
    for (let i = 0; i < array_gift_given_1.length; i++) {
        if (array_gift_given_1.length > array_gift_given_7.length) {
            array_gift_given_7.push('0');
        }
    }
    /////////////////
    $('input[name = "gift_id"]').each(function(i) {
        array_gift_id.push($(this).val());
    });
    array_report_sale.push(array_gift_id);
    //array gift receive

    array_report_sale.push(array_gift_receive_1);
    array_report_sale.push(array_gift_receive_2);
    array_report_sale.push(array_gift_receive_3);
    array_report_sale.push(array_gift_receive_4);
    array_report_sale.push(array_gift_receive_5);
    array_report_sale.push(array_gift_receive_6);
    array_report_sale.push(array_gift_receive_7);
    //array gift given
    array_report_sale.push(array_gift_given_1);
    array_report_sale.push(array_gift_given_2);
    array_report_sale.push(array_gift_given_3);
    array_report_sale.push(array_gift_given_4);
    array_report_sale.push(array_gift_given_5);
    array_report_sale.push(array_gift_given_6);
    array_report_sale.push(array_gift_given_7);

    console.log(array_report_sale)
    const csrf = document.getElementsByName('csrfmiddlewaretoken');
    //const csrf = document.getElementsByName('csrfmiddlewaretoken')
    $.ajax({
        type: 'POST',
        url: 'edit_gift_rp/',
        headers: {
            "X-CSRFToken": csrf[0].value
        },
        data: JSON.stringify({ "array_report_sale": array_report_sale }),

        processData: false,
        contentType: false,
        contentType: 'application/json',
        dataType: "json",
        success: function(resp) {
            alert("Đã sửa thành công!!!")
            for (let i = 0; i < resp.id.length; i++) {
                $("#gift-remain1-scheme2" + resp.id[i]).val(resp.list_gift_remain[i][0])
                $("#gift-remain2-scheme2" + resp.id[i]).val(resp.list_gift_remain[i][1])
                $("#gift-remain3-scheme2" + resp.id[i]).val(resp.list_gift_remain[i][2])
                $("#gift-remain4-scheme2" + resp.id[i]).val(resp.list_gift_remain[i][3])
                $("#gift-remain5-scheme2" + resp.id[i]).val(resp.list_gift_remain[i][4])
                $("#gift-remain6-scheme2" + resp.id[i]).val(resp.list_gift_remain[i][5])
                $("#gift-remain7-scheme2" + resp.id[i]).val(resp.list_gift_remain[i][6])
            }
        },
        error: function(error) {
            console.log(error)
        }
    }); // end ajax
});