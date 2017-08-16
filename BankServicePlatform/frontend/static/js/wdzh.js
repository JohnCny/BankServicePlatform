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

//获取customer信息
var SingleResult = Backbone.Collection.extend({
    url: '/api/customer/' + localStorage.getItem(key_customer_id)
});
$(document).ready(function() {
    var singleResult = new SingleResult;
    var timestamp = new Date().getTime();
    singleResult.url = singleResult.url + "?t=" + timestamp;
    singleResult.fetch({
        beforeSend: sendAuthentication,
        success: function(collection, response, options) {
            if (response.data.bank_card_number != null) {
                response.data.bank_card_number = response.data.bank_card_number.replace(/[\s]/g, '').replace(/(\d{4})(?=\d)/g, "$1 ");
            }
            singleView.render({ result: response.data });
        },
        error: function(collection, response, options) {
            //错误提示
        }
    });
});