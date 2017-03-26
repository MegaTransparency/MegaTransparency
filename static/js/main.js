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
    $(document).mousemove(function(event) {
        mouse_locations.push({'x': event.pageX, 'y': event.pageY})
    });
});