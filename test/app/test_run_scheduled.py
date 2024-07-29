import pkg.app.run_scheduled as module


class TestRunCrawlersScheduled:
    def test_should_run_indefinite(self, mocker):
        mock_config = mocker.patch('pkg.app.run_scheduled.config')
        mock_config.scheduler_seconds = 100

        mock_every = mocker.patch('schedule.every', autospec=True)
        mock_run_pending = mocker.patch('schedule.run_pending', autospec=True)

        mock_sleep = mocker.patch('time.sleep')
        mocker.patch('pkg.app.run_scheduled.run_crawlers')
        active = mocker.Mock(side_effect=[True, False])

        module.run_crawlers_scheduled(active)

        mock_every.assert_called_with(100)
        mock_run_pending.assert_called_with()
        mock_sleep.assert_called_with(1)
