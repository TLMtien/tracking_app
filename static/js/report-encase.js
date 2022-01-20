const report = document.getElementById('report-endcase')
const canvas = document.getElementById('canvas');
const csrf = document.getElementsByName('csrfmiddlewaretoken')

var anh = document.getElementById("screenshotsContainer");


report.addEventListener('submit', e => {
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
        beforeSend: function() {
            $("#loader").removeClass('hidden');
            $("#load-text").html('Đang gửi...');
        },
        success: function(response) {
            $("#loader").addClass('hidden');
            $("#load-text").html('');
            setTimeout(function() {
                alert('Bạn đã gửi thành công');
            }, 100);
        },
        error: function(error) {
            //console.log(error)
            alert('vui long đăng nhập lại')
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