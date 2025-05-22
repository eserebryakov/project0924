class DefaultSetPropertyStrategy:
    def __init__(self, obj, attribute, value):
        self.__obj = obj
        self.__attribute = attribute
        self.__value = value

    def resolve(self):
        self.__obj[self.__attribute] = self.__value
