/* 
//模板
var SingleView = Backbone.View.extend({
    el: "#single_content",
    initialize: function() {},
    render: function(context) {
        //使用underscore这个库，来编译模板
        var template = _.template($("#single_template").html());
        //加载模板到对应的el属性中
        $(this.el).html(template(context));
    },
});
var singleView = new SingleView;

//获取数据
var SingleResult = Backbone.Collection.extend({
    url: '/api/quota/quota_used_record/11'
});
var singleResult = new SingleResult;
singleResult.fetch({
    success: function(collection, response, options) {
        response.data.create_date = GMTToStr(response.data.create_date)
        singleView.render({ result: response.data });

    },
    error: function(collection, response, options) {
        //错误提示
    }
});
*/

//模板
var LoopView = Backbone.View.extend({
    el: "#loop_content",
    initialize: function() {},
    render: function(context) {
        //使用underscore这个库，来编译模板
        var template = _.template($("#loop_template").html());
        //加载模板到对应的el属性中
        $(this.el).html(template(context));
    },
});
var loopView = new LoopView;

//获取customer的billes
var LoopResult = Backbone.Collection.extend({
    url: '/api/customer/quota_billes/' + localStorage.getItem(key_customer_id)
});
var loopResult = new LoopResult;
loopResult.url = getChangePage(loopResult.url);

loopResult.fetch({
    beforeSend: sendAuthentication,
    success: function(collection, response, options) {
        //判断是否json数组
        if (Array.isArray(response.data)) {
            var arr = [];
            for (var i = 0; i < response.data.length; i++) {
                var obj = response.data[i];
                //生成剩余期数的还款bill记录
                obj.create_date = GMTToStr(obj.create_date);
                var period = parseInt(obj.period_remain, 10)
                for (var j = 0; j < period; j++) {
                    var tmp = deepCopy(obj);
                    tmp.period_remain = j + 1;
                    tmp.create_date = addmulMonth(tmp.create_date, j + 1)
                    arr.push(tmp)
                }
            }
            loopView.render({ result: arr });
        } else {
            //生成剩余期数的还款bill记录
            response.data.create_date = GMTToStr(response.data.create_date)
            var period = parseInt(response.data.period_remain, 10)
            var arr = []
            for (var i = 0; i < period; i++) {
                var tmp = deepCopy(response.data);
                tmp.period_remain = i + 1;
                tmp.create_date = addmulMonth(tmp.create_date, i + 1)
                arr.push(tmp)
            }
            loopView.render({ result: arr });
        }

    },
    error: function(collection, response, options) {
        //错误提示
    }
});


//计算和
function getCount() {
    var total = 0;
    $("[name='check_box']:checked").each(function() {
        //alert($(this).val());  
        var period_amount = $(this).parents("tr").find(".period_amount").text();
        total += parseFloat($.trim(period_amount));
    });
    //alert(total.toFixed(2));
    $("#total").html(total.toFixed(2));
}