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
            $("#percent-consumers-reach" + resp.id).val(resp.consumers_reach)
                // document.querySelector('input[name="conversion"]').value = resp.conversion;
            $("#conversion" + resp.id).val(resp.conversion)
        },
        error: function(error) {
            console.log(error)
        }
    }); // end ajax
}); // end click consumer



//Gift

$(document).on('click', '#gift', function() {
    alert('ok')
    var array_report_sale = [];
    var array_total_consumers = [];
    var array_consumers_approached = [];
    var array_consumers_bought = [];
    var array_consumer_id = [];
    $('input[name = "total-consumers"]').each(function(i) {
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
    // $.ajax({
    //     type: 'POST',
    //     url: 'edit_consumer_rp/',
    //     headers: {
    //         "X-CSRFToken": csrf[0].value
    //     },
    //     data: JSON.stringify({ "array_report_sale": array_report_sale }),

    //     processData: false,
    //     contentType: false,
    //     contentType: 'application/json',
    //     dataType: "json",
    //     success: function(resp) {
    //         alert("Đã sửa thành công!!!")
    //     },
    //     error: function(error) {
    //         console.log(error)
    //     }
    // }); // end ajax
});