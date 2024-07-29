import main as module


class TestMain:
    def test_should_call_run_crawlers_scheduled(self, mocker):
        mock_run_crawlers_scheduled = mocker.patch('main.run_crawlers_scheduled')

        module.main()

        mock_run_crawlers_scheduled.assert_called_once()
