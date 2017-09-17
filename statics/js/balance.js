var myChart = echarts.init(document.getElementById('piechart'), 'dark');

var option = {
    tooltip: {
        trigger: 'item',
        formatter: "{b} <br/>HKE {c} ({d}%)"
    },

    visualMap: {
        show: false,
        min: 0,
        max: 1,
        inRange: {
            colorLightness: [0, 1]
        }
    },

    series: [{
        name: 'Currency',
        type: 'pie',
        radius: '90%',
        center: ['50%', '50%'],
        data: [
            { value: 1, name: 'Loading' }
        ],
        roseType: 'radius',
        label: {
            normal: {
                textStyle: {
                    color: 'rgba(255, 255, 255, 0.3)'
                }
            }
        },
        labelLine: {
            normal: {
                lineStyle: {
                    color: 'rgba(255, 255, 255, 0.3)'
                },
                smooth: 0.2,
                length: 10,
                length2: 20
            }
        },
        itemStyle: {
            normal: {
                color: '#1997c6',
                shadowBlur: 200,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
        },

        animationType: 'scale',
        animationEasing: 'elasticOut',
        animationDelay: function(idx) {
            return Math.random() * 200;
        }
    }]
};

myChart.setOption(option);

$(window).on('resize', function() {
    if (myChart != null && myChart != undefined) {
        myChart.resize();
    }
});

(function worker() {

    $.get('api/balance', function(data) {

        $(".balance_row").remove();

        option.series[0].data = _.filter(data, 'in_hkd').map(function(eachData) {

            // populate data for table
            addRow(eachData.ccy, eachData.in_hkd);

            // populate data for chart
            return { name: eachData.ccy, value: eachData.in_hkd };
        }).sort(function(a, b) { return a.value - b.value; });

        addRow("<h6>Total</h6>", _.sumBy(option.series[0].data, 'value'));

        option.visualMap.max = _.maxBy(option.series[0].data, 'value')['value'] * 1.5;
        option.visualMap.min = _.minBy(option.series[0].data, 'value')['value'] * 0.75;

        myChart.setOption(option);
        setTimeout(worker, 10000);
    });
})();

function addRow(ccy, value) {
    e_balance_template = $("#balance_template");
    e_balance_row = e_balance_template.clone();
    e_balance_row.attr("id", "balance_row_" + ccy);
    e_balance_row.toggleClass("balance_template balance_row");

    $(e_balance_row).find(".balance_ccy").html(ccy);
    $(e_balance_row).find(".balance_amt").html(accounting.formatMoney(value, "HKE "));
    e_balance_row.insertBefore(e_balance_template);
}