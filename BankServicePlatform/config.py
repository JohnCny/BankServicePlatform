__author__ = 'Johnny'

DEBUG = True
SECRET_KEY = '\x9c\n)\xec7 ?o@\x86\xc4\xe5_\x00\x10\xd9A$\xd3\x81\xcd\x1d\xb3\x90'

SQLALCHEMY_DATABASE_URI = 'mysql://root:root@192.168.3.252:3306/bank_service_platform'

CELERY_BROKER_URL = 'redis://192.168.3.252:6379/0'

"""
MAIL_DEFAULT_SENDER = 'info@bankserviceplatform.com'
MAIL_SERVER = 'smtp.postmarkapp.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'
"""
SECURITY_POST_LOGIN_VIEW = '/'
SECURITY_PASSWORD_HASH = 'plaintext'
SECURITY_PASSWORD_SALT = 'password_salt'
SECURITY_REMEMBER_SALT = 'remember_salt'
SECURITY_RESET_SALT = 'reset_salt'
SECURITY_RESET_WITHIN = '5 days'
SECURITY_CONFIRM_WITHIN = '5 days'
SECURITY_SEND_REGISTER_EMAIL = False
