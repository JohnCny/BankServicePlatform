//验证码登陆
var Customers = Backbone.Collection.extend({
    url: '/api/login',
    parse: function(response) {
        localStorage.setItem(key_customer_id, 1);
        localStorage.setItem(key_token, "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUwMjc5MjM4NCwiaWF0IjoxNTAyNzA1OTg0fQ.eyJpZCI6NjZ9.r2Uxsm_5YDKdMNrlUof4bYr01qL-w6T_He4NdJnq6jg");

        window.location.href = "wdzh";
    }
});

var customers = new Customers;

$("#subBtn").click(function() {
    customers.create($('#contentForm').serializeJSON());
});