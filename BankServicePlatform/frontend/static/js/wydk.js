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


//获取数据
var Quota_used_record = Backbone.Model.extend({
    url: '/api/quota/quota_used_record',
    parse: function(response) {
        $('#dialog').show();
    }
});
var quota_used_record = new Quota_used_record;
$("#subBtn").click(function() {
    //var obj = [];
    //obj["quota_used_record"] = $('#contentForm').serializeJSON();
    //obj["period"] = $('#period').val();
    var obj = { "quota_used_record": { "quota_id": $('#quota_id').val(), "used_quota": $('#used_quota').val() }, "period": $('#period').val() }
    quota_used_record.save(obj, {
        beforeSend: sendAuthentication
    });
});

//计算金额
function getAmount() {
    var used_quota = $("#used_quota").val();
    var rate = 0.18;
    var period = $("#period").val();
    var total = used_quota * rate * Math.pow((1 + rate), period) / (Math.pow((1 + rate), period) - 1);

    $("#amount").html(total.toFixed(2));
    //return (amount * rate * (1 + rate) ** period) / ((1 + rate) ** period - 1)
}