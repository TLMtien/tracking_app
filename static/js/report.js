const report = document.getElementById('reportPOSM')
const canvas = document.getElementById('canvas');
const csrf = document.getElementsByName('csrfmiddlewaretoken')

//const myfile = document.getElementById('screenshot')
console.log(icon_sales);
canvas.toBlob(function(blob) {
    const formData = new FormData();
    formData.append('my-file', blob, 'filename.png')
        //
    console.log(formData)
    if (report) {
        report.addEventListener('click', e => {
            e.preventDefault()
            console.log('submitted')

            $.ajax({
                type: 'POST',
                url: icon_sales,
                data: {
                    'csrfmiddlewaretoken': csrf[0].value,
                    'image': formData,
                },
                success: function(response) {
                    console.log(response)
                },
                error: function(error) {
                    console.log(error)

                }
            })

        })
    }

})