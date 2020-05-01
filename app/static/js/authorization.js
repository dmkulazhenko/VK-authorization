function getMyUrl() {
    return 'http://0.0.0.0:5000/'
}

function getAjaxInformation(url) {
    let response = null;
    $.ajax({
        type: "GET",
        url: url,
        async: false,
        success: function (text) {
            response = text;
        }
    });
    return response;
}

function postAjaxInformation(url, data) {
    let response = null;
    $.ajax({
        type: "POST",
        url: url,
        async: false,
        data: JSON.stringify(data),
        contentType: 'application/json;charset=UTF-8',
        success: function (text) {
            response = {
                'responseText': text,
                'status': 200
            }
        },
        error: function (xhr, status, error) {
            response = xhr;
        }
    });
    return response
}

$('.vk_logo img').click(function () {
    let response = getAjaxInformation('api/authorize/vk');
    window.location.href = response;
});