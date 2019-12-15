from abc import ABCMeta, abstractmethod


class BaseController:
    __metaclass__ = ABCMeta

    def __init__(self, app, base_path):
        self.__app = app
        self.__base_path = base_path

    def _add_url_rule(self, relative_path, view_function, methods=['GET']):
        self.__app.add_url_rule(self.__base_path + relative_path,
                                view_func=view_function,
                                methods=methods)

    @abstractmethod
    def add_url_rules(self):
        pass
