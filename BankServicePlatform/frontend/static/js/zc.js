var Customers = Backbone.Collection.extend({
    url: '/api/customer',
    parse: function(response) {
        //if(response.data.success)
        window.location.href = "wdzh";
    }
});

var customers = new Customers;

$("#subBtn").click(function() {
    customers.create(JSON.stringify($('#contentForm').serializeJSON()));
});