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

//获取customer所有贷款记录
var LoopResult = Backbone.Collection.extend({
    url: '/api/customer/quota_used_recordes/' + localStorage.getItem(key_customer_id)

});
var loopResult = new LoopResult;

loopResult.fetch({
    beforeSend: sendAuthentication,
    success: function(collection, response, options) {
        if (Array.isArray(response.data)) {
            for (var i = 0; i < response.data.length; i++) {
                var obj = response.data[i];
                obj.create_date = GMTToStr(obj.create_date);
            }
        } else {

        }
        loopView.render({ result: response.data });
    },
    error: function(collection, response, options) {
        //错误提示
    }
});