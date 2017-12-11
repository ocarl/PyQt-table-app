from PyQt5.QtWidgets import *

class WidgetSingleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = QWidget.__new__(class_, *args, **kwargs)
        return class_._instance
