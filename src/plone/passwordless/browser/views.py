from Products.CMFPlone.resources import add_resource_on_request
from Products.Five import BrowserView

class PracticingView(BrowserView):

    def __call__(self):
        # utility function to add resource to rendered page
        add_resource_on_request(self.request, 'practicing')
        return super(PracticingView, self).__call__()