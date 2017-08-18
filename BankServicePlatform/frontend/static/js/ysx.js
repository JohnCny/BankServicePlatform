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

//模板
var BtnView = Backbone.View.extend({
    el: "#btn_content",
    initialize: function() {},
    render: function(context) {
        //使用underscore这个库，来编译模板
        var template = _.template($("#btn_template").html());
        //加载模板到对应的el属性中
        $(this.el).html(template(context));
    },
});
var btnView = new BtnView;

//获取数据
var SingleResult = Backbone.Collection.extend({
    url: '/api/customer/quota/' + localStorage.getItem(key_customer_id)
});
var singleResult = new SingleResult;
singleResult.fetch({
    beforeSend: sendAuthentication,
    success: function(collection, response, options) {
        singleView.render({ result: response.data });
        btnView.render({ result: response.data });
    },
    error: function(collection, response, options) {
        //错误提示
    }
});


function updateQuota() {
    if (submitFlag) {
        submitFlag = false;

    } else {
        return;
    }
    //请求调额
    var UpdateQuotaResult = Backbone.Collection.extend({
        url: '/api/quota/pad_increase_amount/' + $("#quota_id").val()
    });
    var updateQuotaResult = new UpdateQuotaResult;

    updateQuotaResult.url = getChangePage(updateQuotaResult.url);

    updateQuotaResult.fetch({
        beforeSend: sendAuthentication,
        success: function(collection, response, options) {
            if (response.data.result == null || response.data.result != "Failed") {
                $('#dialog').show();
            } else {
                setTimeOut("申请提交失败！！")
            }
        },
        error: function(collection, response, options) {
            //错误提示
        }
    });
}