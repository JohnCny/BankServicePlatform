var Customer =  Backbone.Model.extend({
    url: '/api/customer',
    //解析异步请求返回的结果，fetch方法与save方法都会调用它
    parse: function(res) {
        //保存customeId和token
        //localStorage.setItem(key_customer_id, res.data.customer.id);
        //localStorage.setItem(key_token, res.data.token);
        localStorage.setItem(key_customer_id, 1);
        localStorage.setItem(key_token, "111");
        window.location.href = 'wdzh';
    }
});

var customer = new Customer;
$("#subBtn").click(function() {
    var obj = [];
    obj["customer"] = $('#contentForm').serializeJSON();
    customer.save(obj);
});