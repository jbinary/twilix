from twisted.internet import task

from twilix.jid import internJID

class BasePattern(object):
    def __init__(self, myjid, keepalive_period=None):
        """ :param myjid: The jid of the component."""

        self.myjid = internJID(myjid)
        if keepalive_period is not None:
            self.keepalive_period = keepalive_period
            self.keepalive_send_task = task.LoopingCall(self.send_keepalive)

    def send_keepalive(self):
        self.xmlstream.transport.write(' ')

    def startSendingKeepalives(self):
        if hasattr(self, 'keepalive_period'):
            self.keepalive_send_task.start(self.keepalive_period)

    def stopSendingKeepalives(self):
        if hasattr(self, 'keepalive_period'):
            self.keepalive_send_task.stop()
