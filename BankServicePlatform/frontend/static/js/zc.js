var Customer =  Backbone.Model.extend({
    url: '/api/customer',
    //解析异步请求返回的结果，fetch方法与save方法都会调用它
    parse: function(res) {
        return res.data;
    }
});

var Customers = Backbone.Collection.extend({
    url: '/api/customer',
    parse: function(response) {
        alert(111)
        window.location.href = "wdzh";
    }
});

var customers = new Customers;

$("#subBtn").click(function() {
    //var obj = new Object();
    //obj.customer = $('#contentForm').serializeJSON();
    //var data = { "customer": JSON.stringify($('#contentForm').serializeJSON()) };
    //alert(data);

    var data = '{ "customer":' + JSON.stringify($('#contentForm').serializeJSON());
    var customer = new Customer;
    //customer.set({ "customer": JSON.stringify($('#contentForm').serializeJSON()) });
    customer.save(data);
});