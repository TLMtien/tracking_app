// const report = document.getElementById('reportPOSM')
// const canvas = document.getElementById('canvas');
// const csrf = document.getElementsByName('csrfmiddlewaretoken')
//     //var icon_sales = "{% url 'reportPosm' %}"
//     //const myfile = document.getElementById('screenshot')
// var anh = document.getElementById("screenshotsContainer");


// //var anh2 = anh1.
// //var screen = document.getElementById('screenshotsContainer');


// report.addEventListener('click', e => {
//         e.preventDefault()
//         var image = document.getElementById("canvas").toDataURL("image/png")
//             .replace("image/png", "image/octet-stream");
//         //console.log(anh)

//         console.log(image)


//         $.ajax({
//             type: 'POST',
//             url: icon_sales,

//             data: {
//                 //
//                 'image': image,
//                 'csrfmiddlewaretoken': csrf[0].value,
//             },
//             success: function(response) {
//                 alert('success')
//             },
//             error: function(error) {
//                 console.log(error)

//             }
//         })

//     })
//     // var image = document.getElementById("screenshot")
//     //     //         .replace("image/png", "image/octet-stream");

// // if (report) {
// //     report.addEventListener('click', e => {
// //         e.preventDefault()
// //         console.log(icon_sales);

// //         canvas.toBlob(function(blob) {
// //             const formData = new FormData();
// //             formData.append('canvas', blob, 'filename.png')
// //             formData.append('csrfmiddlewaretoken', csrf[0].value)
// //                 //console.log(formData.get('filename.png'))
// //             console.log(formData)

// //             $.ajax({
// //                 type: 'POST',
// //                 url: icon_sales,
// //                 enctype: 'multipart/form-data',
// //                 data: {
// //                     'image': formData,
// //                 },
// //                 success: function(response) {
// //                     alert('ok')
// //                 },
// //                 error: function(error) {
// //                     console.log(error)
// //                 },
// //                 cache: false,
// //                 contentType: false,
// //                 processData: false,
// //             })


// //         })

// //     })
// // }





const report = document.getElementById('reportPOSM')
const canvas = document.getElementById('canvas');
const csrf = document.getElementsByName('csrfmiddlewaretoken')

var anh = document.getElementById("screenshotsContainer");


report.addEventListener('click', e => {
    e.preventDefault()
    var image = document.getElementById("canvas").toDataURL("image/png")

    var blobFile = dataURItoBlob(image)
    console.log(blobFile);
    var file = new File([blobFile], new Date().getTime(), { type: blobFile.type });


    console.log(file)

    var fd = new FormData();
    fd.append("image", file);
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
            alert('Bạn đã gửi thành công')
        },
        error: function(error) {
            console.log(error)

        }
    });

});


function dataURItoBlob(dataURI) {
    // convert base64/URLEncoded data component to raw binary data held in a string
    var byteString;
    if (dataURI.split(',')[0].indexOf('base64') >= 0)
        byteString = atob(dataURI.split(',')[1]);
    else
        byteString = unescape(dataURI.split(',')[1]);
    // separate out the mime component
    var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    // write the bytes of the string to a typed array
    var ia = new Uint8Array(byteString.length);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ia], { type: mimeString });
}