$(function() {
    $(window).unload(function(){
        console.log('leaving');
        $.ajax({
            type: 'POST',
            url: '/api/update_page_view',
            async:false,
            data: {uuid:page_view_uuid, data: '{}'}
        });
    });
});