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
    url: '/api/customer/quota/' + localStorage.getItem(key_customer_id)
});
var singleResult = new SingleResult;
singleResult.fetch({
    beforeSend: sendAuthentication,
    success: function(collection, response, options) {
        singleView.render({ result: response.data });
    },
    error: function(collection, response, options) {
        //错误提示
    }
});

$("#btn1").click(function() {
    //请求调额
    var QuotaResult = Backbone.Collection.extend({
        url: '/api/quota/pad_increase_amount/' + $("#quota_id").val()
    });
    var quotaResult = new QuotaResult;

    quotaResult.fetch({
        beforeSend: sendAuthentication,
        success: function(collection, response, options) {
            $('#dialog').show();
        },
        error: function(collection, response, options) {
            //错误提示
        }
    });
});