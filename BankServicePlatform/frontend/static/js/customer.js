/**
 * Created by Johnny on 2017/8/7 0007.
 */

var Customer = Backbone.Model.extend({
    urlRoot: '/api/customer'
});

var Customers = Backbone.Collection.extend({
    url: '/api/customer',
    model: Customer,
    parse: function(response) {
        return response.data;
    }
});

var CustomerRouter = Backbone.Router.extend({
    routes: {
        "customer/:customer_id": "showCustomer"
    },

    showCustomer: function(customer_id) {

    }

});


var customers = new Customers();

customers.fetch({
    success: function(collection, response, options) {

    },
    error: function(collection, response, options) {

    }
});

var newCustomer = customers.create({
    real_name: $('#real_name'),
    phone: $('#phone'),
    identification_number: $('#identification_number'),
    password: $('#password'),
    channel: '1'
});