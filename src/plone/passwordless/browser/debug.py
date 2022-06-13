from collections import OrderedDict

from Products.Five.browser import BrowserView


class Debug(BrowserView):

    def getInstanceDict(self):
        result = OrderedDict()
        for k in sorted(self.context.__dict__.keys()):
            result[k] = self.context.__dict__[k]
        return result
