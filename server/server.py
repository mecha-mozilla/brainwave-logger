# -*- coding: utf-8 -*- 
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, World")

class LoggingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Logging")
        brainlog = {"url"        : self.get_argument("url"),
                    "id"         : self.get_argument("id"),
                    "attention"  : self.get_argument("attention"),
                    "meditation" : self.get_argument("meditation"),
                    "delta"      : self.get_argument("delta"),
                    "theta"      : self.get_argument("theta"),
                    "lowalpha"   : self.get_argument("lowalpha"),
                    "highalpha"  : self.get_argument("highalpha"),
                    "lowbeta"    : self.get_argument("lowbeta"),
                    "highbeta"   : self.get_argument("highbeta"),
                    "lowgamma"   : self.get_argument("lowgamma"),
                    "highgamma"  : self.get_argument("highgamma"),
                    "like"       : self.get_argument("like")}

        self.write(str(brainlog))

class LearningHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Learning")

    def post(self):
        self.set_handler("Content-Type", "text/plain")
        brain = self.get_argument("brain")
        web   = self.get_argument("web")
        self.write("You wrote " + self.get_argument("message"))

class TestingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Testing")

    def post(self):
        self.set_handler("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("message"))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/log/", LoggingHandler),
    (r"/learn/", LearningHandler),
    (r"/test/", TestingHandler)
])


if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

