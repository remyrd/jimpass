from jimpass.parser import Parser

template_str = "account <b>{name}</b> with user {username}"
mapping = {
    'name': 'name',
    'username': 'login.username'
}

parser = Parser(
    template_str,
    mapping
)

dummy_item = {
    "name": "Bob",
    "login": {
        "username": "sponge.bob"
    }
}
dummy_str = "account <b>Bob</b> with user sponge.bob"

dummy_incomplete_item = {
    "name": "Bob"
}
dummy_incomplete_str = "account <b>Bob</b> with user ?"  # intentionally missing


def test_dump():
    assert(parser.dumps(parser.flat_map_item(dummy_item)) == dummy_str)


def test_load():
    loaded_item = parser.loads(dummy_str)
    for field in loaded_item.keys():
        assert(field in mapping)
    loaded_incomplete_item = parser.loads(dummy_incomplete_str)
    assert(loaded_incomplete_item['name'] == dummy_incomplete_item['name'])
