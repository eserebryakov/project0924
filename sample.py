class IoCContainer:
    @staticmethod
    def _strategy(dependency: str, *args):
        return 1

    @staticmethod
    def resolve(dependency: str, *args):
        return IoCContainer._strategy(dependency, *args)


def scope_create_empty():
    return {}


def scope_create():
    ...


def register():
    ...


def scope_current():
    ...


root_scope = {
    "IoC.Scope.Current": 2,
    "IoC.Scope.Create.Empty": scope_create_empty,
}


ioc_scope = IoCContainer.resolve("IoC.Scope.Create")
print(ioc_scope)
