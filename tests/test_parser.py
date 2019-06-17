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


def test_dump():
    assert(parser.dumps(dummy_item) == dummy_str)


def test_load():
    loaded_item = parser.loads(dummy_str)
    assert('name' in loaded_item and 'login' in loaded_item)
    assert(loaded_item['name'] == dummy_item['name'])
    assert(loaded_item['login']['username'] == dummy_item['login']['username'])
