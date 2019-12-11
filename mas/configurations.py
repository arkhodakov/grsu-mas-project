class BaseCongig(object):
	DEBUG = True
	TESTING = False
	TEMPLATES_AUTO_RELOAD = True
 
class ProductionConfig(BaseCongig):
	DEBUG = False
 
class DevelopmentConfig(BaseCongig):
	DEBUG = True
	TESTING = True
