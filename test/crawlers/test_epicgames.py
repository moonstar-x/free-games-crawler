import pkg.crawlers.epicgames as module
import pytest
import pathlib
import json
from pkg.models.offer import Offer


@pytest.fixture(scope='session')
def mocked_epic_games_data():
    cur_directory = pathlib.Path(__file__).parent.resolve()
    filepath = cur_directory.joinpath('__mocks__/epic_games_response.txt')

    with filepath.open('r') as file:
        return json.loads(file.read())


@pytest.fixture
def crawler(mocked_epic_games_data, mocker):
    mock_client = mocker.MagicMock()
    mock_client.get_json.return_value = mocked_epic_games_data

    return module.EpicGamesCrawler(mock_client)


class TestEpicGamesCrawler:
    class TestRun:
        def test_should_return_offers(self, crawler):
            result = list(crawler.run())

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


class TestBuilder:
    def test_should_have_correct_name(self):
        assert module.Builder.NAME == 'EpicGames'

    class TestMake:
        def test_should_return_valid_instance(self):
            assert isinstance(module.Builder.make(), module.EpicGamesCrawler)
