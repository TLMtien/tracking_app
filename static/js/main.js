const outletForm = document.getElementById('outlet-form')
    //const provinceInput = document.getElementById('province')
    //const districtInput = document.getElementById('district')
const table = document.getElementById('list_table_search')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

if (outletForm) {
    outletForm.addEventListener('submit', e => {
        e.preventDefault()
        console.log('submitted')
        const provinceInput = document.getElementById('aaa')
        const districtInput = document.getElementById('bbb')

        const outlet_id = document.getElementById('outlet-id')

        console.log(provinceInput.value)
        console.log(districtInput.value)
        console.log(outlet_id.value)
        var fd = new FormData();
        fd.append("district", districtInput.value);
        fd.append("outletID", outlet_id.value),
            $.ajax({
                type: 'POST',
                url: icon_sales,
                headers: {
                    "X-CSRFToken": csrf[0].value
                },
                data: fd,
                processData: false,
                contentType: false,

                success: function(response) {
                    //alert('ok')
                    console.log(response)
                    outlet_id.value = ""
                    table.innerHTML = response.list_outlet
                },
                error: function(error) {
                    console.log(error)

                }
            })
    })
}