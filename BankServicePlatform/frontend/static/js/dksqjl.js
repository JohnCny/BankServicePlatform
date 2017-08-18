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

loopResult.url = getChangePage(loopResult.url);
loopResult.fetch({
    beforeSend: sendAuthentication,
    success: function(collection, response, options) {

        var tmp = []
        if (Array.isArray(response.data)) {
            tmp = response.data;
        } else {
            if (response.data != null) {
                tmp.push(response.data)
            }
        }
        for (var i = 0; i < tmp.length; i++) {
            var obj = tmp[i];
            if (obj != null && obj.create_date != null) {
                obj.create_date = GMTToStr(obj.create_date);
            }
        }
        loopView.render({ result: tmp });
    },
    error: function(collection, response, options) {
        //错误提示
    }
});