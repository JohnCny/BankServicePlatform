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

//获取customer信息
var LoopResult = Backbone.Collection.extend({
    url: '/api/customer/' + localStorage.getItem(key_customer_id)
});
var loopResult = new LoopResult;
loopResult.fetch({
    beforeSend: sendAuthentication,
    success: function(collection, response, options) {
        //判断是否json数组
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
            if (obj != null && obj.bank_card_number != null) {
                obj.bank_card_number = obj.bank_card_number.replace(/[\s]/g, '').replace(/(\d{4})(?=\d)/g, "$1 ");
            }
        }
        loopView.render({ result: tmp });
    },
    error: function(collection, response, options) {
        //错误提示
    }
});

//更换银行卡
var Card = Backbone.Model.extend({
    url: '/api/customer/' + localStorage.getItem(key_customer_id) + '/add_bank_card',
    parse: function(response) {
        window.location.href = 'wydk'
    }
});
var card = new Card;
$("#subBtn").click(function() {
    var obj = [];
    obj["customer"] = { "bank_card_number": $("#bank_card_number").val() };
    card.save(obj, {
        beforeSend: sendAuthentication
    });
});