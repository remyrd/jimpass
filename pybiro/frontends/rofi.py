""" Calls Rofi on the system """
from pybiro.util import srun
from pybiro.frontends.base import Frontend


class Rofi(Frontend):

    def __init__(self, config):
        Frontend.__init__(self)
        self.call_display_types = {
            'user_input': self._user_input
        }

    """
    TODO: enforce type_ supported by particular frontend before it's called by the backend
    """
    def display(self, **kwargs):
        """
        Call either of two methods configured: `user_input` or `menu` through type_
        :param kwargs: must containe at least type_
        :return:
        """
        if "type_" not in kwargs.keys():
            raise Exception("Rofi requires one of two `user_input` or `menu` under type_")
        return self.call_display_types[kwargs["type_"]](kwargs)

    """
    TODO: make this more generic and translate into Rofi arguments/params
    """
    def _user_input(self, kwargs: dict):
        kwargs.pop("type_")
        return "rofi " + " ".join([f"-{k} {v}" for k, v in kwargs.items()])

    @property
    def display_types(self):
        return ['user_input']



def run(**kwargs):
    """ Run Rofi """
    args = " ".join([f"-{k} {v}" for k, v in kwargs.items()])
    return srun(f"rofi {args}")
