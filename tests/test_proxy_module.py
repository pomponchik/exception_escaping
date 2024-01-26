import asyncio

import pytest

import escape
from escape.errors import SetDefaultReturnValueForDecoratorError


def test_run_simple_function():
    some_value = 'kek'

    @escape
    def function():
        return some_value

    assert function() == some_value


def test_run_simple_function_with_some_arguments():
    @escape
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_function_with_exception():
    @escape
    def function(a, b, c=5):
        raise ValueError

    function(1, 2)


def test_run_coroutine_function():
    some_value = 'kek'

    @escape
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


def test_run_coroutine_function_with_some_arguments():
    @escape
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


def test_run_coroutine_function_with_exception():
    @escape
    async def function(a, b, c=5):
        raise ValueError

    asyncio.run(function(1, 2))


def test_run_simple_function_with_empty_brackets():
    some_value = 'kek'

    @escape()
    def function():
        return some_value

    assert function() == some_value


def test_run_simple_function_with_some_arguments_with_empty_brackets():
    @escape()
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_function_with_exception_with_empty_brackets():
    @escape()
    def function(a, b, c=5):
        raise ValueError

    function(1, 2)


def test_run_coroutine_function_with_empty_brackets():
    some_value = 'kek'

    @escape()
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


def test_run_coroutine_function_with_some_arguments_with_empty_brackets():
    @escape()
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


def test_run_coroutine_function_with_exception_with_empty_brackets():
    @escape()
    async def function(a, b, c=5):
        raise ValueError

    asyncio.run(function(1, 2))


def test_run_simple_function_with_default_return():
    some_value = 'kek'

    @escape(default_return='lol')
    def function():
        return some_value

    assert function() == some_value


def test_run_simple_function_with_some_arguments_with_default_return():
    @escape(default_return='lol')
    def function(a, b, c=5):
        return a + b + c

    assert function(1, 2) == 8
    assert function(1, 2, 5) == 8
    assert function(1, 2, c=5) == 8
    assert function(1, 2, c=8) == 11


def test_run_function_with_exception_with_default_return():
    default_value = 13

    @escape(default_return=default_value)
    def function(a, b, c=5):
        raise ValueError

    assert function(1, 2) == default_value


def test_run_coroutine_function_with_default_return():
    some_value = 'kek'

    @escape(default_return='lol')
    async def function():
        return some_value

    assert asyncio.run(function()) == some_value


def test_run_coroutine_function_with_some_arguments_with_default_return():
    @escape(default_return='lol')
    async def function(a, b, c=5):
        return a + b + c

    assert asyncio.run(function(1, 2)) == 8
    assert asyncio.run(function(1, 2, 5)) == 8
    assert asyncio.run(function(1, 2, c=5)) == 8
    assert asyncio.run(function(1, 2, c=8)) == 11


def test_run_coroutine_function_with_exception_with_default_return():
    default_value = 13

    @escape(default_return=default_value)
    async def function(a, b, c=5):
        raise ValueError

    assert asyncio.run(function(1, 2)) == default_value


def test_wrong_argument_to_decorator():
    with pytest.raises(ValueError, match='You are using the decorator for the wrong purpose.'):
        escape('kek')


def test_context_manager_with_empty_brackets_muted_by_default_exception():
    with escape():
        raise ValueError


def test_context_manager_with_empty_brackets_not_muted_by_default_exception():
    for not_muted_exception in (GeneratorExit, KeyboardInterrupt, SystemExit):
        with pytest.raises(not_muted_exception):
            with escape():
                raise not_muted_exception


def test_context_manager_with_exceptions_parameter_not_muted_exception():
    with pytest.raises(ValueError):
        with escape(exceptions=(ZeroDivisionError,)):
            raise ValueError

    with pytest.raises(ValueError):
        with escape(exceptions=[ZeroDivisionError]):
            raise ValueError


def test_context_manager_with_exceptions_parameter_muted_exception():
    for muted_exception in (GeneratorExit, KeyboardInterrupt, SystemExit):
        with escape(exceptions=(muted_exception,)):
            raise muted_exception

    for muted_exception in (GeneratorExit, KeyboardInterrupt, SystemExit):
        with escape(exceptions=[muted_exception]):
            raise muted_exception


def test_context_manager_without_breackets_muted_exception():
    for muted_exception in (ValueError, KeyError, Exception):
        with escape:
            raise muted_exception


def test_context_manager_without_breackets_not_muted_exception():
    for not_muted_exception in (GeneratorExit, KeyboardInterrupt, SystemExit):
        with pytest.raises(not_muted_exception):
            with escape:
                raise not_muted_exception


def test_decorator_without_breackets_saves_name_of_function():
    @escape
    def function():
        pass

    assert function.__name__ == 'function'


def test_decorator_without_breackets_saves_name_of_coroutine_function():
    @escape
    async def function():
        pass

    assert function.__name__ == 'function'


def test_context_manager_with_default_return_value():
    with pytest.raises(SetDefaultReturnValueForDecoratorError, match='You cannot set a default value for the context manager. This is only possible for the decorator.'):
        with escape(default_return='lol'):
            ...

def test_set_exceptions_types_with_bad_typed_value():
    with pytest.raises(ValueError, match='The list of exception types can be of the list or tuple type.'):
        escape(exceptions='lol')


def test_set_exceptions_types_with_bad_typed_exceptions_in_list():
    with pytest.raises(ValueError, match='The list of exception types can contain only exception types.'):
        escape(exceptions=[ValueError, 'lol'])


def test_decorator_with_list_of_muted_exceptions():
    @escape(exceptions=[ValueError])
    def function():
        raise ValueError

    function()


def test_decorator_with_list_of_not_muted_exceptions():
    @escape(exceptions=[ValueError])
    def function():
        raise KeyError

    with pytest.raises(KeyError):
        function()


def test_decorator_with_tuple_of_muted_exceptions():
    @escape(exceptions=(ValueError, ))
    def function():
        raise ValueError

    function()


def test_decorator_with_list_of_not_muted_exceptions():
    @escape(exceptions=(ValueError,))
    def function():
        raise KeyError

    with pytest.raises(KeyError):
        function()


def test_async_decorator_with_list_of_muted_exceptions():
    @escape(exceptions=[ValueError])
    async def function():
        raise ValueError

    asyncio.run(function())


def test_async_decorator_with_list_of_not_muted_exceptions():
    @escape(exceptions=[ValueError])
    async def function():
        raise KeyError

    with pytest.raises(KeyError):
        asyncio.run(function())


def test_async_decorator_with_tuple_of_muted_exceptions():
    @escape(exceptions=(ValueError, ))
    async def function():
        raise ValueError

    asyncio.run(function())


def test_async_decorator_with_list_of_not_muted_exceptions():
    @escape(exceptions=(ValueError,))
    async def function():
        raise KeyError

    with pytest.raises(KeyError):
        asyncio.run(function())


def test_default_default_value_is_none():
    @escape(exceptions=(ValueError,))
    def function():
        raise ValueError

    assert function() is None


def test_default_default_value_is_none_in_async_case():
    @escape(exceptions=(ValueError,))
    async def function():
        raise ValueError

    assert asyncio.run(function()) is None
