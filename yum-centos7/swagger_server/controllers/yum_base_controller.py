from .base_controller import BaseController


class YumBaseController(BaseController):

    def __init__(self, app, base_path, yum_base):
        super(YumBaseController, self).__init__(app, base_path)
        self.__yum_base = yum_base