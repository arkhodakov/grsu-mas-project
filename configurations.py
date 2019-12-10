class BaseCongig(object):
	DEBUG = True
	TESTING = False
 
class ProductionConfig(BaseCongig):
	DEBUG = False
 
class DevelopmentConfig(BaseCongig):
	DEBUG = True
	TESTING = True
