/**
 * Created by boss on 16-7-26.
 */
$(document).ready(function () {
    $('#wordcloud_button').click(function () {
        var v = $('#queryword').val();
        var ul = $('#lists_contain_queryword');
        var ul1 = $('#songs_appear_manytimes');

        $.getJSON('wordcloud', {'queryword': v}, function (ret) {

            var lists_to_show = ret['lists_contain_queryword'];
            var songs_to_show = ret['songs_appaer_manytimes'];
            // clear all the list items within ul and ul1 except the first ones
            ul.find("li:first-child").nextAll().remove();
            ul1.find("li:first-child").nextAll().remove();
            // define a function to add li to ul and ul1
            function modify_list(list, data) {

                var add_item = function (elem) {

                    var li = $('<li><a href="#"></a></li>');
                    var l = li.find('a');
                    if (elem.length === 2) {
                        l.attr('href', elem[1]);
                        l.text(elem[0]);
                        list.append(li);
                    }
                    else {

                        l.attr('href', 'http://music.163.com/song?id=' + elem[2]);
                        l.text(elem[0] + '          ' + elem[1] + '次');
                        list.append(li);
                    }

                };
                data.map(add_item);
            }

            modify_list(ul, lists_to_show);
            modify_list(ul1, songs_to_show);
            // if the list is empty, then add one item to the list telling
            // the user that no song appears more than twice
            if (ul1.children('li').length - 1 === 0) {
                var warning = $('<li>没有出现多次的歌曲(╬￣皿￣)凸</li>');
                ul1.append(warning);
            }
        });
    });
});
