import pkg.models.offer as module


class TestOffer:
    class TestToJson:
        def test_should_return_correct_json_string(self):
            offer = module.Offer(
                storefront='Store',
                url='https://store.com/game',
                title='Game',
                description='A game that is fun.',
                type='game',
                publisher='GamesCorp',
                original_price=19.99,
                original_price_fmt='$19.99',
                thumbnail='https://store.com/game/thumbnail.jpg'
            )

            assert offer.to_json() == '{"storefront": "Store", "url": "https://store.com/game", "title": "Game", "description": "A game that is fun.", "type": "game", "publisher": "GamesCorp", "original_price": 19.99, "original_price_fmt": "$19.99", "thumbnail": "https://store.com/game/thumbnail.jpg"}'

        def test_should_return_correct_json_string_with_nullable_properties(self):
            offer = module.Offer(
                storefront='Store',
                url='https://store.com/game',
                title='Game',
                description='A game that is fun.',
                type='game',
                publisher=None,
                original_price=None,
                original_price_fmt=None,
                thumbnail=None
            )

            assert offer.to_json() == '{"storefront": "Store", "url": "https://store.com/game", "title": "Game", "description": "A game that is fun.", "type": "game", "publisher": null, "original_price": null, "original_price_fmt": null, "thumbnail": null}'

    class TestEq:
        def test_should_return_true_for_equal_offers(self):
            offer1 = module.Offer(
                storefront='Store',
                url='https://store.com/game',
                title='Game',
                description='A game that is fun.',
                type='game',
                publisher='GamesCorp',
                original_price=19.99,
                original_price_fmt='$19.99',
                thumbnail='https://store.com/game/thumbnail.jpg'
            )

            offer2 = module.Offer(
                storefront='Store',
                url='https://store.com/game',
                title='Game',
                description='A game that is fun.',
                type='game',
                publisher='GamesCorp',
                original_price=19.99,
                original_price_fmt='$19.99',
                thumbnail='https://store.com/game/thumbnail.jpg'
            )

            assert offer1 == offer2

        def test_should_return_false_for_unequal_offers(self):
            offer1 = module.Offer(
                storefront='Stores',
                url='https://store.com/game',
                title='Game',
                description='A game that is fun.',
                type='game',
                publisher='GamesCorp',
                original_price=19.99,
                original_price_fmt='$19.99',
                thumbnail='https://store.com/game/thumbnail.jpg'
            )

            offer2 = module.Offer(
                storefront='Store',
                url='https://store.com/game',
                title='Game',
                description='A game that is fun.',
                type='game',
                publisher='GamesCorp',
                original_price=19.99,
                original_price_fmt='$19.99',
                thumbnail='https://store.com/game/thumbnail.jpg'
            )

            assert offer1 != offer2
