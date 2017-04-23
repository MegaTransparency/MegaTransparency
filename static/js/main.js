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
    Vue.component('mttable', {
        delimiters: ['${', '}'],
            template: '#table-template',
        props: ['data', 'columns', 'rows']
        });
    var app = new Vue({
      el: '#app',
      data: {
        message: 'Hello Vue!',
          is_logged_in: false,
          table_data: {},
      },
      delimiters: ['${', '}'],
      created: function() {
          window.app = this;
          $.get('/api/is_logged_in', function(data) {
              app.is_logged_in=data.is_logged_in
          })
      },
        methods: {'run_sql_query': function() {
            url = 'https://megatransparency.com/api/query_public_data?sql='+encodeURIComponent($('#sql_query').val());
            $.get(url, function(data) {
                app.$set(app, 'table_data', Object.assign({}, app.table_data, data));
            })
            
        }}
    })
});