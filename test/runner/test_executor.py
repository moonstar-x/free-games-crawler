import pkg.runner.executor as module
import pytest
from unittest.mock import call
from collections import namedtuple
from typing import cast
from pkg.config import Config


class Mocks:
    ConfigMock = namedtuple('ConfigMock', ['threading_enabled', 'threading_max_workers'])


class TestRunnerExecutorOptions:
    class TestFromConfig:
        def test_should_create_options_with_provided_values(self):
            config = cast(Config, Mocks.ConfigMock(
                threading_enabled=False,
                threading_max_workers=5
            ))
            result = module.RunnerExecutorOptions.from_config(config)

            assert result.enabled is False
            assert result.max_workers == 5

        def test_should_create_options_with_default_values(self):
            config = cast(Config, Mocks.ConfigMock(
                threading_enabled=None,
                threading_max_workers=None
            ))
            result = module.RunnerExecutorOptions.from_config(config)

            assert result.enabled is True
            assert result.max_workers == 'auto'


@pytest.fixture
def executor_no_multi(mocker):
    mocker.patch('pkg.runner.executor.Logger', return_value=mocker.MagicMock())

    config = cast(Config, Mocks.ConfigMock(
        threading_enabled=False,
        threading_max_workers='auto'
    ))
    options = module.RunnerExecutorOptions.from_config(config)

    return module.RunnerExecutor(options)


@pytest.fixture
def executor_multi(mocker):
    mocker.patch('pkg.runner.executor.Logger', return_value=mocker.MagicMock())

    config = cast(Config, Mocks.ConfigMock(
        threading_enabled=True,
        threading_max_workers=2
    ))
    options = module.RunnerExecutorOptions.from_config(config)

    return module.RunnerExecutor(options)


@pytest.fixture
def runner(mocker):
    return mocker.MagicMock()


class TestRunnerExecutor:
    class TestInit:
        def test_should_raise_if_max_workers_is_less_than_1(self):
            config = cast(Config, Mocks.ConfigMock(
                threading_enabled=True,
                threading_max_workers=0
            ))
            options = module.RunnerExecutorOptions.from_config(config)

            with pytest.raises(ValueError) as error:
                module.RunnerExecutor(options)
                assert str(error) == 'max_workers must be greater than or equal to 1.'

        def test_should_raise_if_max_workers_is_not_auto_string(self):
            config = cast(Config, Mocks.ConfigMock(
                threading_enabled=True,
                threading_max_workers='something'
            ))
            options = module.RunnerExecutorOptions.from_config(config)

            with pytest.raises(ValueError) as error:
                module.RunnerExecutor(options)
                assert str(error) == 'max_workers must be an integer or "auto".'

        def test_should_raise_if_max_workers_is_something_else(self):
            config = cast(Config, Mocks.ConfigMock(
                threading_enabled=True,
                threading_max_workers=0.5
            ))
            options = module.RunnerExecutorOptions.from_config(config)

            with pytest.raises(ValueError) as error:
                module.RunnerExecutor(options)
                assert str(error) == 'max_workers must be an integer or "auto".'

    class TestPush:
        def test_should_add_runner_to_queue(self, executor_no_multi, runner):
            assert executor_no_multi._runners.qsize() == 0
            executor_no_multi.push(runner)
            assert executor_no_multi._runners.qsize() == 1
            executor_no_multi.push(runner)
            assert executor_no_multi._runners.qsize() == 2

    class TestStart:
        class TestSingleThread:
            def test_should_log_start_message(self, executor_no_multi):
                executor_no_multi.start()
                executor_no_multi._logger.info.assert_any_call('Begin single thread execution.')

            def test_should_execute_all_runners_in_queue(self, executor_no_multi, runner):
                executor_no_multi.push(runner)
                executor_no_multi.push(runner)
                executor_no_multi.start()

                runner.run.assert_has_calls([call()] * 2)

        class TestMultiThread:
            def test_should_log_start_message(self, executor_multi):
                executor_multi.start()
                executor_multi._logger.info.assert_any_call('Begin multi thread execution with 2 workers.')

            def test_should_execute_all_runners_in_queue(self, executor_multi, runner):
                executor_multi.push(runner)
                executor_multi.push(runner)
                executor_multi.start()

                runner.run.assert_has_calls([call()] * 2)
