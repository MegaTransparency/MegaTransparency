$(function() {
    $(window).unload(function(){
        $.ajax({
            type: 'POST',
            url: '/api/update_page_view',
            async:false,
            data: {page_view_uuid:page_view_uuid}
        });
    });
});