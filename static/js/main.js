function debounce(delay, callback) {
    var timeout = null;
    return function () {
        //
        // if a timeout has been registered before then
        // cancel it so that we can setup a fresh timeout
        //
        if (timeout) {
            clearTimeout(timeout);
        }
        var args = arguments;
        timeout = setTimeout(function () {
            callback.apply(null, args);
            timeout = null;
        }, delay);
    };
}
$(function() {
    window.mouse_locations = []
    $(window).on("unload", function(e) {
        console.log('leaving');
        var data = {};
        data["screen_width"] = screen.width;
        data["screen_height"] = screen.height;
        data["mouse_locations"] = window.mouse_locations;
        console.log(JSON.stringify(data));
        $.ajax({
            type: 'POST',
            url: '/api/update_page_view',
            async: false,
            data: {uuid:page_view_uuid, data: JSON.stringify(data)}
        });
    });
    $(document).mousemove(debounce(250, function(event) {
        mouse_locations.push({'x': event.pageX, 'y': event.pageY})
    }));
});