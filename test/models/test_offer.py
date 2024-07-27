import pkg.models.offer as module


class TestOffer:
    class TestToJson:
        def test_should_return_correct_json_string(self):
            offer = module.Offer(
                storefront='Store'
            )

            assert offer.to_json() == '{"storefront": "Store"}'
