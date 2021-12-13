const report = document.getElementById('reportPOSM')
const canvas = document.getElementById('canvas');
const csrf = document.getElementsByName('csrfmiddlewaretoken')
    //var icon_sales = "{% url 'reportPosm' %}"
    //const myfile = document.getElementById('screenshot')
var anh = document.getElementById("screenshotsContainer");


//var anh2 = anh1.
//var screen = document.getElementById('screenshotsContainer');


report.addEventListener('click', e => {
        e.preventDefault()
        var image = document.getElementById("canvas").toDataURL("image/png")
            .replace("image/png", "image/octet-stream");
        //console.log(anh)

        console.log(image)


        $.ajax({
            type: 'POST',
            url: icon_sales,

            data: {
                //
                'image': image,
                'csrfmiddlewaretoken': csrf[0].value,
            },
            success: function(response) {
                alert('success')
            },
            error: function(error) {
                console.log(error)

            }
        })

    })
    // var image = document.getElementById("screenshot")
    //     //         .replace("image/png", "image/octet-stream");

// if (report) {
//     report.addEventListener('click', e => {
//         e.preventDefault()
//         console.log(icon_sales);

//         canvas.toBlob(function(blob) {
//             const formData = new FormData();
//             formData.append('canvas', blob, 'filename.png')
//             formData.append('csrfmiddlewaretoken', csrf[0].value)
//                 //console.log(formData.get('filename.png'))
//             console.log(formData)

//             $.ajax({
//                 type: 'POST',
//                 url: icon_sales,
//                 enctype: 'multipart/form-data',
//                 data: {
//                     'image': formData,
//                 },
//                 success: function(response) {
//                     alert('ok')
//                 },
//                 error: function(error) {
//                     console.log(error)
//                 },
//                 cache: false,
//                 contentType: false,
//                 processData: false,
//             })


//         })

//     })
// }