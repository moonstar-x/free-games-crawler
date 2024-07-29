import pkg.utils.log as module


class TestLogger:
    def test_should_print_log_with_tag(self, capfd):
        tag = 'mytag'
        logger = module.Logger(tag)

        message = 'my message'
        logger.info(message)

        out, err = capfd.readouterr()
        assert tag in out

    def test_should_print_log_message_single(self, capfd):
        tag = 'mytag'
        logger = module.Logger(tag)

        message = 'my message'
        logger.info(message)

        out, err = capfd.readouterr()
        assert message in out

    def test_should_print_log_message_multi(self, capfd):
        tag = 'mytag'
        logger = module.Logger(tag)

        message1 = 'my message'
        message2 = 'another message'
        logger.info(message1, message2)

        out, err = capfd.readouterr()
        assert message1 in out
        assert message2 in out

    def test_should_print_exception_with_tag(self, capfd):
        tag = 'mytag'
        logger = module.Logger(tag)

        try:
            raise Exception()
        except Exception as error:
            logger.exception(error)

        out, err = capfd.readouterr()
        assert tag in out

    def test_should_print_exception(self, capfd):
        tag = 'mytag'
        logger = module.Logger(tag)

        message = 'Oops'
        try:
            raise Exception(message)
        except Exception as error:
            logger.exception(error)

        out, err = capfd.readouterr()

        assert 'Exception' in out
        assert message in out
        assert 'Traceback' in out
