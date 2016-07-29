/**
 * Created by boss on 16-7-26.
 */
$(document).ready(function () {
    $('#wordcloud_button').click(function () {
        var v = $('#queryword').val();
        var ul = $('#lists_contain_queryword');
        $.get('wordcloud', {'queryword': v}, function (ret) {
            var lists = ret['lists_contain_queryword'];
            ul.children('li').remove();
            var add_item = function (elem) {
                var li = $('<li></li>');
                li.text(elem);
                ul.append(li);
            };
            lists.map(add_item);
        });
    });
});
