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

$('.vk_logo img').click(function () {
    let response = getAjaxInformation('api/authorize/vk');
    window.location.href = response;
});