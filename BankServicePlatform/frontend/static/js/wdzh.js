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

var singleResult = new SingleResult;

singleResult.url = getChangePage(singleResult.url);
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

//模板
var QuotaView = Backbone.View.extend({
    el: "#quota_content",
    initialize: function() {},
    render: function(context) {
        //使用underscore这个库，来编译模板
        var template = _.template($("#quota_template").html());
        //加载模板到对应的el属性中
        $(this.el).html(template(context));
    },
});
var quotaView = new QuotaView;

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
var QuotaResult = Backbone.Collection.extend({
    url: '/api/customer/quota/' + localStorage.getItem(key_customer_id)
});

var quotaResult = new QuotaResult;

quotaResult.url = getChangePage(quotaResult.url);

quotaResult.fetch({
    beforeSend: sendAuthentication,
    success: function(collection, response, options) {
        quotaView.render({ result: response.data });
        btnView.render({ result: response.data });
    },
    error: function(collection, response, options) {
        //错误提示
    }
});

//模板
var RepaymentView = Backbone.View.extend({
    el: "#repayment_content",
    initialize: function() {},
    render: function(context) {
        //使用underscore这个库，来编译模板
        var template = _.template($("#repayment_template").html());
        //加载模板到对应的el属性中
        $(this.el).html(template(context));
    },
});
var repaymentView = new RepaymentView;


//获取数据
var RepaymentResult = Backbone.Collection.extend({
    url: '/api/quota/quota_repayment/' + localStorage.getItem(key_customer_id) + '/get_expected_repayment_7d'
});

var repaymentResult = new RepaymentResult;

repaymentResult.url = getChangePage(repaymentResult.url);

repaymentResult.fetch({
    beforeSend: sendAuthentication,
    success: function(collection, response, options) {
        repaymentView.render({ result: response.data.data });
    },
    error: function(collection, response, options) {
        //错误提示
    }
});