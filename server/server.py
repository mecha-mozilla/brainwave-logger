# -*- coding: utf-8 -*- 
import tornado.ioloop
import tornado.web
import MySQLdb
import json

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

        connector = MySQLdb.connect(host="localhost", db="braindb", user="brainusr", passwd="F6KdbshzQsNySmCn", charset="utf8")
        cursor = connector.cursor()
        sql = u"insert into braindata values(NULL, '"+ brainlog['id'] +"', CURRENT_TIMESTAMP, '"+ brainlog['url'] +"', '"+ brainlog['like'] +"', \
                                            '"+ brainlog['delta'] +"', '"+ brainlog['theta'] +"', '"+ brainlog['lowalpha'] +"', '"+ brainlog['highalpha'] +"', \
                                            '"+ brainlog['lowbeta'] +"', '"+ brainlog['highbeta'] +"', '"+ brainlog['lowgamma'] +"', '"+ brainlog['highgamma'] +"', \
                                            '"+ brainlog['attention'] + "', '"+ brainlog['meditation'] +"')"
        cursor.execute(sql)
        connector.commit()
        cursor.close()
        connector.close()
        self.write("OK")

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

class ShowingHandler(tornado.web.RequestHandler):
    def get(self):
        f = open("header.html", 'r')
        for line in f:
            self.write(line)

        f.close()
        self.write("<body>")
        self.write("<h1> This is Your Brainwave </h1>")
        connector = MySQLdb.connect(host="localhost", db="braindb", user="brainusr", passwd="F6KdbshzQsNySmCn", charset="utf8")
        cursor = connector.cursor()
        sql = 'SELECT user, address, atn, delta, theta, h_alpha, l_alpha, h_beta, l_beta FROM braindata ORDER BY datanum DESC LIMIT 30'
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        connector.close()
        
        self.write('<script type="text/javascript" >')
        self.write('var timer = "1000"; function ReloadAddr(){window.location.reload();}setTimeout(ReloadAddr, timer);')
        self.write('</script>')
        
        self.write('<svg width="640" height="480">')
        for row in rows:
            self.write('\n<circle cx="'+ str(int(row[3])%640) + '" cy="' +str(int(row[4])%480) +'" r="'+ str(int(row[2])) 
                        +'" fill="rgba('+str(int(row[5])%255)+','+str(int(row[6])%255)+','+str(int(row[7])%255)+',30)" opacity="0.3"/>')
            self.write('\n<text x="'+ str(int(row[3])%640) + '" y="' +str(int(row[4])%480)+ '">'+ str(row[1]) +'</text>')
        self.write('</svg>')
        self.write('<form name="button"> <input type="button" value="go" onClick="move()"></form>')
        self.write('</body>')


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/log/", LoggingHandler),
    (r"/learn/", LearningHandler),
    (r"/test/", TestingHandler),
    (r"/show/", ShowingHandler)
])


if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

