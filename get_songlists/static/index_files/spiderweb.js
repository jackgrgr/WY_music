/**
 * Created by gr on 16-7-23.
 */

$(document).ready(function () {
    $('#spiderweb_button').click(function () {
        var v = $("#query_id").val();

        $.get('spiderweb', {'query_id': v}, function (ret) {
            $(function () {

                $('#container').highcharts({

                    chart: {
                        polar: true,
                        type: 'line'
                    },

                    title: {
                        text: '歌单指数查询结果',
                        x: -80
                    },

                    pane: {
                        size: '80%'
                    },

                    xAxis: {
                        categories: ['播放指数', '收藏指数', '分享指数', '评论指数'],
                        tickmarkPlacement: 'on',
                        lineWidth: 0
                    },

                    yAxis: {
                        gridLineInterpolation: 'polygon',
                        lineWidth: 0,
                        min: 0,
                        max: 1
                    },

                    tooltip: {
                        shared: true,
                        pointFormat: '<span style="color:{series.color}">{series.name}: <b>{point.y:,.2f}</b><br/>'
                    },

                    legend: {
                        align: 'right',
                        verticalAlign: 'top',
                        y: 70,
                        layout: 'vertical'
                    },

                    series: [{
                        name: '目标查询歌单',
                        data: [ret['play_index'], ret['fav_index'], ret['share_index'], ret['comment_index']],
                        pointPlacement: 'on'
                    },
                        {
                            name: '歌单平均水平',
                            data: [0.5, 0.5, 0.5, 0.5],
                            pointPlacement: 'on'
                        }
                    ]

                });
            })
        });
    })
});

