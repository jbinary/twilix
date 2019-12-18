from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from twisted.words.protocols.jabber import component

from twilix.patterns import BasePattern
from twilix.dispatcher import Dispatcher

class TwilixComponent(BasePattern, component.Service):
    """ Class to build XMPP components based on twilix. (see XEP-0114)

    Look at the connect method to connect your component to an XMPP-server."""

    DispatcherClass = Dispatcher

    def connect(self, port, secret, host=None):
        """ Connect component to an XMPP-server to make it works.

        :param port: port to connect to. Needs to be set the same as in XMPP
        server config.

        :param secret: a secret to connect to XMPP server.

        :param host: a host to connect to XMPP server. It's needed only
        if host to connect is differ from jid."""

        if host is None:
            host = str(self.myjid)
        f = component.componentFactory(str(self.myjid), secret)
        connector = component.buildServiceManager(str(self.myjid), secret,
                                         "tcp:%s:%s" % (host, port))
        self.setServiceParent(connector)
        connector.startService()

    def componentConnected(self, xs):
        self.xmlstream = xs
        self.dispatcher = self.DispatcherClass(xs, self.myjid)
        self.init()

        self.xmlstream.rawDataInFn = self.rawIn
        self.xmlstream.rawDataOutFn = self.rawOut
        self.startSendingKeepalives()

    def componentDisconnected(self):
        self.stopSendingKeepalives()

    def init(self):
        """ To be overriden in derived classes. Used to initialize all needed
        services """

    def rawIn(self, data):
        print("<<< %s" % data)

    def rawOut(self, data):
        print(">>> %s" % data)
