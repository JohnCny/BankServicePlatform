//注册
var Customer =  Backbone.Model.extend({
    url: '/api/customer',
    //解析异步请求返回的结果，fetch方法与save方法都会调用它
    parse: function(res) {
        if (res.data.result == null || res.data.result != "Failed") {
            //保存customeId和token
            localStorage.setItem(key_customer_id, res.data.data.customer.id);
            localStorage.setItem(key_token, res.data.data.token);
            //localStorage.setItem(key_customer_id, 1);
            //localStorage.setItem(key_token, "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUwMjc5MjM4NCwiaWF0IjoxNTAyNzA1OTg0fQ.eyJpZCI6NjZ9.r2Uxsm_5YDKdMNrlUof4bYr01qL-w6T_He4NdJnq6jg");
            changePage('wdzh');
        } else {
            setTimeOut(res.data.info)
        }

    }
});

var customer = new Customer;
$("#subBtn").click(function() {
    //验证
    var real_name = $("input[name='real_name']").val();
    if (!Validator.VerityLib.IsNotEmpty(real_name) ||
        !Validator.VerityLib.IsChineseCharacter(real_name) ||
        !Validator.VerityLib.IsStringLength(real_name, 2, 4)) {
        setTimeOut("请填写正确的姓名！")
        return;
    }
    var phone = $("input[name='phone']").val();
    if (!Validator.VerityLib.IsNotEmpty(phone) ||
        !Validator.VerityLib.IsMobilePhoneNumber(phone)) {
        setTimeOut("请填写正确的手机号码！")
        return;
    }
    var identification_number = $("input[name='identification_number']").val();
    if (!Validator.VerityLib.IsNotEmpty(identification_number) ||
        !Validator.VerityLib.IsIDCard(identification_number)) {
        setTimeOut("请填写正确的身份证号码！")
        return;
    }

    customer.url = getChangePage(customer.url);
    var obj = [];
    obj["customer"] = $('#contentForm').serializeJSON();
    customer.save(obj, {});
});