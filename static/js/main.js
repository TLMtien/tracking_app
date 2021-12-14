const outletForm = document.getElementById('outlet-form')
    //const provinceInput = document.getElementById('province')
    //const districtInput = document.getElementById('district')
const provinceInput = document.getElementById('aaa')
const districtInput = document.getElementById('bbb')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

if (outletForm) {
    outletForm.addEventListener('submit', e => {
        e.preventDefault()
        console.log('submitted')

        $.ajax({
            type: 'POST',
            url: '/outlet/search/',
            data: {
                'csrfmiddlewaretoken': csrf[0].value,
                'province': provinceInput.value,
                'district': districtInput.value,
            },
            success: function(response) {
                console.log(response)
                    //$('h2').html(response)
            },
            error: function(error) {
                console.log(error)

            }
        })
    })
}




//--------------------------------------------------------------

// const reportPOSM = document.getElementById('reportPOSM')
// const canvas = document.getElementById('canvas');
// var image = document.getElementById("canvas").toDataURL("image/png")
//     .replace("image/png", "image/octet-stream");
// const myfile = document.getElementById('screenshot')



// reportPOSM.addEventListener('submit', e => {
//     e.preventDefault()
//     console.log('submitted')

//     $.ajax({
//         type: 'POST',
//         url: "{% url 'reportPosm' %}",
//         data: {
//             'csrfmiddlewaretoken': csrf[0].value,
//             'image': image,
//         },
//         success: function(response) {
//             console.log(response)
//         },
//         error: function(error) {
//             console.log(error)

//         }
//     })
// })