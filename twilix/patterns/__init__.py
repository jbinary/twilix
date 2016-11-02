from twilix.jid import internJID

class BasePattern(object):
    def __init__(self, myjid):
        """ :param myjid: The jid of the component."""
        self.myjid = internJID(myjid)
