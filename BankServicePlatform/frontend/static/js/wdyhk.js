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

//获取数据
var LoopResult = Backbone.Collection.extend({
    url: '/api/quota/quota_bill/2/repayment'
});
var loopResult = new LoopResult;
loopResult.fetch({
    beforeSend: sendAuthentication,
    success: function(collection, response, options) {
        //判断是否json数组
        if (Array.isArray(response.data)) {
            loopView.render({ result: [{}, {}, {}] });
        } else {
            loopView.render({ result: [{}, {}, {}] });
        }

    },
    error: function(collection, response, options) {
        //错误提示
    }
});