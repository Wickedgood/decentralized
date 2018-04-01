import inspect
import logging
# Logger.debug(), Logger.info(), Logger.warning(), Logger.error(), and Logger.critical
path = "files/"
logger = logging.getLogger('root')

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(filename=path + 'runlog.log', level=logging.DEBUG, format=FORMAT)