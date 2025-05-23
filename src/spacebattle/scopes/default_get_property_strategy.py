class DefaultGetPropertyStrategy:
    def __init__(self, obj, attribute):
        self.__obj = obj
        self.__attribute = attribute

    def resolve(self):
        return self.__obj[self.__attribute]
