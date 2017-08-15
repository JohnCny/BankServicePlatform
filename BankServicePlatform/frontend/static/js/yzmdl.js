var Customers = Backbone.Collection.extend({
    url: '/api/login',
    parse: function(response) {
        window.location.href = "wdzh";
    }
});

var customers = new Customers;

$("#subBtn").click(function() {
    customers.create($('#contentForm').serializeJSON());
});