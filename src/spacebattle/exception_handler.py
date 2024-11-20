from queue import Queue

from src.spacebattle.commands import (
    Command,
    DefaultCommand,
    PutCommand,
    Retry2Command,
    RetryCommand,
    WriteCommand,
)


class DefaultException(Exception):
    ...


class ExceptionHandler:
    store = {}

    @staticmethod
    def handle(command: Command, exception: Exception) -> Command:
        ct, et = type(command), type(exception)
        return ExceptionHandler.store.get(ct, {et: lambda c, e: DefaultCommand(command=c, exception=e)}).get(
            et, lambda c, e: DefaultCommand(command=c, exception=e)
        )(command, exception)

    @staticmethod
    def register_handler(command_type: type, exception_type: type, handler) -> None:
        ExceptionHandler.store[command_type] = {exception_type: handler}


def exception_handler_put_command(command: Command, exception: Exception, queue: Queue) -> None:
    """Обработчик исключения, который ставит Команду в очередь Команд."""
    ExceptionHandler.register_handler(
        command_type=type(command),
        exception_type=type(exception),
        handler=lambda c, _: PutCommand(command=command, queue=queue),
    )


def exception_handler_put_write_command(command: Command, exception: Exception, queue: Queue) -> None:
    """Обработчик исключения, который ставит Команду, пишущую в лог в очередь Команд."""
    write_command = WriteCommand(command=command, exception=exception)
    ExceptionHandler.register_handler(
        command_type=type(command),
        exception_type=type(exception),
        handler=lambda c, _: PutCommand(command=write_command, queue=queue),
    )


def exception_handler_put_repeater_command(command: Command, exception: Exception, queue: Queue) -> None:
    """Обработчик исключения, который ставит в очередь Команду - повторитель команды, выбросившей исключение."""
    ExceptionHandler.register_handler(
        command_type=type(command),
        exception_type=type(exception),
        handler=lambda c, _: PutCommand(command=RetryCommand(command=c), queue=queue),
    )


def exception_handler_once_repeat_command(command: Command, exception: Exception, queue: Queue) -> None:
    """Стратегия обработки исключений: при первом выбросе исключения повторить команду,
    при повторном выбросе исключения записать информацию в лог"""
    write_command = WriteCommand(command=command, exception=exception)
    ExceptionHandler.register_handler(
        command_type=type(command),
        exception_type=type(exception),
        handler=lambda c, _: PutCommand(command=RetryCommand(command=c), queue=queue),
    )
    ExceptionHandler.register_handler(
        command_type=type(RetryCommand(None)),
        exception_type=type(exception),
        handler=lambda c, _: PutCommand(command=write_command, queue=queue),
    )


def exception_handler_twice_repeat_command(command: Command, exception: Exception, queue: Queue) -> None:
    """Стратегия обработки исключений: обработки исключения - повторить два раза, потом записать в лог"""
    write_command = WriteCommand(command=command, exception=exception)
    ExceptionHandler.register_handler(
        command_type=type(command),
        exception_type=type(exception),
        handler=lambda c, _: PutCommand(command=RetryCommand(command=c), queue=queue),
    )
    ExceptionHandler.register_handler(
        command_type=type(RetryCommand(None)),
        exception_type=type(exception),
        handler=lambda c, _: PutCommand(command=Retry2Command(command=command), queue=queue),
    )
    ExceptionHandler.register_handler(
        command_type=type(Retry2Command(None)),
        exception_type=type(exception),
        handler=lambda c, _: PutCommand(command=write_command, queue=queue),
    )
