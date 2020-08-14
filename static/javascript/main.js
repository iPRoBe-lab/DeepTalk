
// run on ducument read
$('document').ready(function () {

});

// Text input and GET request
function loading(ennable) {
    if (ennable) {
        $('#loader').removeClass('gone');
        $("input[type=button]").attr("disabled", "disabled");
    } else {
        $('#loader').addClass('gone');
        $("input[type=button]").removeAttr("disabled");
    }
}

////////////////
// Load Samples
////////////////

$("#csv-input").change(function () {

    loading(true)

    var file = document.getElementById('csv-input').files[0];
    var reader = new FileReader();
    var isSuccess = checkCSVFileType(file);

    if (isSuccess) {
        reader.onload = function (event) {
            var csvData = event.target.result;
            process(csvData);
        };
        if (file) {
            reader.readAsText(file);
        }
    } else {
        alert('incorrect file type, please upload a CSV file with headings.')
    }

});

$('document').ready(function () {

    $('#csv-sample').click(function () {
        loading(true)

        $.ajax({
            url: 'static/sample.csv',
            dataType: 'text',
        }).done(process);

    });

    $('#csv-download').click(function () {

        $.ajax({
            url: 'static/sample.csv',
            dataType: 'text',
        }).done(download);

    });

});

function download() {
    document.getElementById('download').click();
}

function process(csvData) {

    data = $.csv.toObjects(csvData);
    if (data && data.length > 0) {
        fillTable($('#table-results'), data);
        sendPostRequest(data);
    } else {
        alert('File is empty!');
    }

}

function sendPostRequest(request) {

    $('#error').html("");
    console.log(request);
    request = JSON.stringify(request);

    $.ajax({
        method: "POST",
        url: "./api/post",
        data: { "request": request }
    }).done(function (response) {

        if (response.hasOwnProperty('error')) {
            $('#error').html(response['error']);
            console.log(response['error']);
        }
        else {
            console.log(response);
        }
        loading(false);
    });
}

function checkCSVFileType(file) {
    fileTypes = ['csv'];
    extension = file.name.split('.').pop().toLowerCase();
    return fileTypes.indexOf(extension) > -1;
};

function fillTable(table, data, samples = -1) {

    console.log(table)
    h = data[0]
    keys = Object.keys(h)

    if (samples == -1) {
        samples = data.length
    }

    html = '<table class="table table-sm" id="table">'
    for (i = 0; i < keys.length; i++) {
        if (i % 2 == 1) {
            html += '<col class="bg-light">'
        }
        else {
            html += '<col>'
        }
    }
    html += '<thead>'
    html += '<tr>'

    for (i = 0; i < keys.length; i++) {
        k = keys[i]
        html += '<th>' + k + '</th>'
    }

    html += '</tr>'
    html += '</thead>'
    html += '<tbody>'

    for (i = 0; i < samples && i < data.length; i++) {
        html += '<tr>'

        for (j = 0; j < keys.length; j++) {
            k = keys[j]
            d = data[i][k]

            html += '<td>' + d + '</td>'
        }

        html += '<tr>'
    }

    html += '</tbody>'
    table.append(html);

}

//////////////
// Input Field
//////////////

$('#text-input').keydown(function (e) {
    var data = $('#text-input').val();
    if (e.which == 13 && data.length > 0) {
        sendGetRequest(data);
    }
});

$('#text-submit').click(function (e) {
    var data = $('#text-input').val();
    if (data.length > 0) {
        sendGetRequest(data);
    };
});

function sendGetRequest(request) {

    loading(true);
    $('#error').html('')
    console.log(request);

    $('#error').html("");
    $('#text-input').val('');

    $.ajax({
        method: "GET",
        url: "./api/get",
        data: { "request": request }
    }).done(function (response) {

        if (response.hasOwnProperty('error')) {
            $('#error').html(response['error']);
            console.log(response['error']);
        }
        else {
            console.log(response);
        }
        loading(false);
    });
}

//////////////
// Image input
//////////////

$("#img-input").change(function () {

    loading(true);
    var preview = document.getElementById('img');

    $('#img-results').html('')
    $('#img-loader').removeClass('gone')

    var file = document.getElementById('img-input').files[0];
    var isSuccess = checkImageType(file);
    var reader = new FileReader();

    if (isSuccess) {
        reader.addEventListener("load", function () {
            preview.src = reader.result;
            preview.style.display = 'inline'
            preview.style.height = '100%';

            var form = new FormData($('#form')[0]);

            $.ajax({
                url: '/api/image',
                type: 'POST',
                data: form,
                cache: false,
                processData: false,
                contentType: false,
            }).done(function (response) {
                $('#error').html('')

                if (response.hasOwnProperty('error')) {
                    $('#error').html(response['error'])
                    console.log(response['error']);
                }
                else {
                    console.log(response);
                }
                loading(false);

            });


        }, false);

        if (file) {
            reader.readAsDataURL(file);
        }

    } else {
        alert('incorrect file type, please upload a JPG, JPEG, or PNG image.')
    }

});

function checkImageType(file) {
    fileTypes = ['jpg', 'jpeg', 'png'];
    extension = file.name.split('.').pop().toLowerCase()
    return fileTypes.indexOf(extension) > -1;
}
