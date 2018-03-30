import inspect
import logging
import User
# Logger.debug(), Logger.info(), Logger.warning(), Logger.error(), and Logger.critical
'''
logger = logging.getLogger('root')

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename='runlog.log', level=logging.DEBUG, format=FORMAT)
'''
xyfz = User.User("xyfz","This is my password")
adam = User.User("adam","This is not xyfz password")
