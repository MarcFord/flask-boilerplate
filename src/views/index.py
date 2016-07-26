from lib.ext.view.base_view import BaseView


class IndexView(BaseView):

    def index(self):
        return self.render('index/index.html')
