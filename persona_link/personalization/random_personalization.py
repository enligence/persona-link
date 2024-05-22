from .models import Personalization
from .base import PersonalizationBase
from random import choice
class RandomPersonalization(PersonalizationBase):
    def __init__(self):
        # generate many templates for prefix and suffix given name and role (optional)
        pass

    async def personalize(self, text: str, name: str, role: str=None) -> Personalization:
        # randomly select one template for prefix and suffix
        # replace {name} with the name and {role} with the role
        # return the Personalization object
        prefix = choice(self.prefix_templates).format(name=name, role=role)
        suffix = choice(self.suffix_templates).format(name=name, role=role)
        return Personalization(prefix=prefix, suffix=suffix)