import pkg.crawlers.epicgames as module
import pytest
import pathlib
import json
from pkg.models.offer import Offer


def read_mocked_data(path):
    cur_directory = pathlib.Path(__file__).parent.resolve()
    filepath = cur_directory.joinpath(path)

    with filepath.open('r') as file:
        return json.loads(file.read())


@pytest.fixture(scope='session')
def mocked_epic_games_data_1():
    return read_mocked_data('__mocks__/epic_games_response-1.txt')


@pytest.fixture(scope='session')
def mocked_epic_games_data_2():
    return read_mocked_data('__mocks__/epic_games_response-2.txt')


@pytest.fixture
def crawler_1(mocked_epic_games_data_1, mocker):
    mock_client = mocker.MagicMock()
    mock_client.get_json.return_value = mocked_epic_games_data_1

    return module.EpicGamesCrawler(mock_client)


@pytest.fixture
def crawler_2(mocked_epic_games_data_2, mocker):
    mock_client = mocker.MagicMock()
    mock_client.get_json.return_value = mocked_epic_games_data_2

    return module.EpicGamesCrawler(mock_client)


class TestEpicGamesCrawler:
    class TestRun:
        def test_should_return_offers_response_1(self, crawler_1):
            result = list(crawler_1.run())

            offer_1 = Offer(
                storefront='EpicGames',
                id='fist-forged-in-shadow-torch',
                url='https://store.epicgames.com/p/fist-forged-in-shadow-torch',
                title='F.I.S.T.: Forged In Shadow Torch',
                description='Explore more than a dozen unique areas in a Metroidvania style map. \nThe Fist, Drill, and Whip are three weapons with completely different fighting styles that offer seamless switching between high combo, high damage, and long range attacks. ',
                type='game',
                publisher='Antiidelay',
                original_price=29.99,
                original_price_fmt='$29.99',
                thumbnail='https://cdn1.epicgames.com/offer/a7e2a2c51b9149c097b771926ed91877/EGS_FISTForgedInShadowTorch_TiGames_S6_1200x1600-b0ce396c042359ad9a7b2ca50726cac1'
            )

            offer_2 = Offer(
                storefront='EpicGames',
                id='olympics-go-paris-2024-pc-outfits-a48737',
                url='https://store.epicgames.com/p/olympics-go-paris-2024-pc-outfits-a48737',
                title='Exclusive Outfits Pack',
                description='Rep your love for the Olympic Games Paris 2024 and stand out from the crowd with these 11 unique outfits featuring the official mascot!',
                type='dlc',
                publisher='nWay Inc',
                original_price=54.99,
                original_price_fmt='$54.99',
                thumbnail='https://cdn1.epicgames.com/spt-assets/16c163a44eea408c94b388cb63aafe6d/olympics-go-paris-2024-1gk76.jpg'
            )

            assert result[0] == offer_1
            assert result[1] == offer_2

        def test_should_return_offers_response_2(self, crawler_2):
            result = list(crawler_2.run())

            offer = Offer(
                storefront='EpicGames',
                id='hot-wheels-unleashed',
                url='https://store.epicgames.com/p/hot-wheels-unleashed',
                title='HOT WHEELS UNLEASHED™',
                description='HOT WHEELS UNLEASHED™',
                type='other',
                publisher='Epic Dev Test Account',
                original_price=0.0,
                original_price_fmt='0',
                thumbnail='https://cdn1.epicgames.com/offer/d5241c76f178492ea1540fce45616757/EGS_HolidaySale_2024_GameArt_Game10_1080x1920_1920x1080-da542ce3d442311a86d81c40b5d87691'
            )

            assert result[0] == offer


class TestBuilder:
    def test_should_have_correct_name(self):
        assert module.Builder.NAME == 'EpicGames'

    class TestMake:
        def test_should_return_valid_instance(self):
            assert isinstance(module.Builder.make(), module.EpicGamesCrawler)
