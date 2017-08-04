__author__ = 'Johnny'

from flask.ext.script import Manager, Server

from BankServicePlatform import app

manager = Manager(app)

server = Server(host='0.0.0.0', port=8888)
manager.add_command("runserver", server)

if __name__ == '__main__':
    manager.run()