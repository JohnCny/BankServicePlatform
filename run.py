__author__ = 'Johnny'

# from flask_script import Manager, Server
#
# from BankServicePlatform import app
#
# manager = Manager(app)
#
# server = Server(host='127.0.0.1', port=8888)
# manager.add_command("runserver", server)
#
# if __name__ == '__main__':
#     manager.run()

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from BankServicePlatform import api,frontend

application=DispatcherMiddleware(frontend.create_app(),{
    '/api':api.create_app()
})

if __name__=="__main__":
    run_simple('0.0.0.0',5000,application,use_reloader=True,use_debugger=True,threaded=True)