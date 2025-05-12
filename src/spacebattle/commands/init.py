import threading

from src.spacebattle.commands.clear_current_scope import ClearCurrentScopeCommand
from src.spacebattle.commands.command import Command
from src.spacebattle.commands.register_dependency import RegisterDependencyCommand
from src.spacebattle.commands.set_current_scope import SetCurrentScopeCommand
from src.spacebattle.common import constants
from src.spacebattle.exceptions.exeptions import ParentScopeMissingException
from src.spacebattle.scopes.dependency_resolver import DependencyResolver
from src.spacebattle.scopes.ioc import IoC


def _ioc_scope_parent():
    raise ParentScopeMissingException("Отсутствует родительский scope")


def _ioc_scope_create(*args):
    creating_scope = IoC.resolve(constants.IOC_SCOPE_CREATE_EMPTY)
    if args:
        parent_scope = args[0]
        creating_scope[constants.IOC_SCOPE_PARENT] = lambda *a: parent_scope
    else:
        parent_scope = IoC.resolve(constants.IOC_SCOPE_CURRENT)
        creating_scope[constants.IOC_SCOPE_PARENT] = lambda *a: parent_scope
    return creating_scope


class InitCommand(Command):
    root_scope = dict()
    current_scope = threading.local()
    already_executed_successfully = False

    def execute(self):
        if InitCommand.already_executed_successfully:
            return

        with threading.Lock():
            InitCommand.root_scope[constants.IOC_SCOPE_CURRENT_SET] = lambda *args: SetCurrentScopeCommand(*args)
            InitCommand.root_scope[constants.IOC_SCOPE_CURRENT_CLEAR] = lambda *args: ClearCurrentScopeCommand()
            InitCommand.root_scope[constants.IOC_SCOPE_CURRENT] = (
                lambda *args: InitCommand.current_scope.value
                if hasattr(InitCommand.current_scope, "value")
                else InitCommand.root_scope
            )
            InitCommand.root_scope[constants.IOC_SCOPE_PARENT] = lambda *args: _ioc_scope_parent()
            InitCommand.root_scope[constants.IOC_SCOPE_CREATE_EMPTY] = lambda *args: {}
            InitCommand.root_scope[constants.IOC_SCOPE_CREATE] = lambda *args: _ioc_scope_create(*args)
            InitCommand.root_scope[constants.IOC_REGISTER] = lambda dependency, strategy: RegisterDependencyCommand(
                dependency=dependency, strategy=strategy
            )
            IoC.resolve(
                constants.UPDATE_IOC_RESOLVE_DEPENDENCY_STRATEGY,
                lambda old_strategy: lambda dependency, *args: DependencyResolver(
                    InitCommand.current_scope.value
                    if hasattr(InitCommand.current_scope, "value")
                    else InitCommand.root_scope
                ).resolve(dependency, *args),
            ).execute()

            InitCommand.already_executed_successfully = True
