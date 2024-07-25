import pkg.utils.list as module


class TestListFind:
    arr = [1, 2, 3, 4, 5]
    complex_arr = [{'a': 0}, {'b': 'b'}]

    def test_should_return_none_if_not_found(self):
        result = module.list_find(TestListFind.arr, lambda i: False)
        assert result is None

    def test_should_return_item_if_found(self):
        result = module.list_find(TestListFind.arr, lambda i: i == 3)
        assert result is 3

    def test_should_return_item_if_found_complex_array(self):
        result = module.list_find(TestListFind.complex_arr, lambda obj: obj.get('b') == 'b')
        assert result['b'] == 'b'

    def test_should_return_item_if_predicate_is_not_boolean(self):
        result = module.list_find(TestListFind.complex_arr, lambda obj: obj.get('b'))
        assert result['b'] == 'b'
