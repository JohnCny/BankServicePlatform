var Customers = Backbone.Collection.extend({
    url: '/api/login',
    parse: function(response) {
        //if(response.data.success)
        localStorage.setItem(appid, response.data)
        window.location.href = "wdzh";
    }
});

var customers = new Customers;

$("#subBtn").click(function() {
    customers.create(JSON.stringify($('#contentForm').serializeJSON()));
});