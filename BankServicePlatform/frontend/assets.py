# -*- coding: utf-8 -*-
__author__ = 'Johnny'

from flask_assets import Environment, Bundle


#: application css bundle
css_bankserviceplatform = Bundle("less/bankserviceplatform.less",
                       filters="less", output="css/bankserviceplatform.css",
                       debug=False)

#: consolidated css bundle
css_all = Bundle("css/main.css", css_bankserviceplatform,
                 filters="cssmin", output="css/bankserviceplatform.min.css")

#: vendor js bundle
js_quote = Bundle("js/quote/jquery-3.2.1.min.js",
                   "js/quote/underscore-1.8.3.min.js",
                   "js/quote/backbone-1.3.3.min.js")

#: application js bundle
# js_customer = Bundle("coffee/*.coffee", filters="coffeescript", output="js/customer.js")
js_customer = Bundle("js/customer.js")

def init_app(app):
    webassets = Environment(app)
    webassets.register('css_all', css_all)
    # webassets.register('js_quote', js_quote)
    # webassets.register('js_main', js_customer)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug