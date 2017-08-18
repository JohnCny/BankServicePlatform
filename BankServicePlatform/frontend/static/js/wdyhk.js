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
            if (obj.bank_card_number == "0") {
                obj.bank_card_number = "未绑定银行卡"
            }
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
    parse: function(res) {
        if (res.data.result == null || res.data.result != "Failed") {
            changePage('wydk')
        } else {
            setTimeOut(res.data.info)
        }
    }
});
var card = new Card;
$("#subBtn").click(function() {
    //验证
    var bank_card_number = $("input[name='bank_card_number']").val();
    if (!Validator.VerityLib.IsNotEmpty(bank_card_number) ||
        !Validator.VerityLib.IsIntegerNotNagtive(bank_card_number) ||
        !Validator.VerityLib.IsBankCard(bank_card_number)) {
        setTimeOut("请填写正确的卡号！")
        return;
    }
    var obj = [];
    obj["customer"] = { "bank_card_number": $("#bank_card_number").val() };


    singlcardeResult.url = getChangePage(singleResult.url);
    card.save(obj, {
        beforeSend: sendAuthentication
    });
});