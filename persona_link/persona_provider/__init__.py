from persona_link.persona_provider.azure import AzureAvatar
from persona_link.persona_provider.base import PersonaBase
from persona_link.persona_provider.heygen import HeygenAvatar
from persona_link.persona_provider.sprite import SpriteAvatar

persona_link_providers = {}

def persona_link_provider(klass):
    name = getattr(klass, "name", None)
    desc = getattr(klass, "description", None)
    
    if not isinstance(name, str) or not isinstance(desc, str):
        raise TypeError(f"In {klass}, name or description are not strings")
    
    if not name:
        raise ValueError(f"{klass} class should define a non-empty name attribute")
    if not desc:
        raise ValueError(
            f"{klass} class should define a non-empty description attribute"
        )
        
    if name in persona_link_providers:
        raise ValueError(f"In class {klass}: Provider with name {name} already exists")
    
    persona_link_providers[name] = klass
    
    print(f"Registered persona provider: {name}")
    
    def inner(*args, **kwargs):
        return klass(*args, **kwargs)

    return inner

__all__ = [ "AzureAvatar", "PersonaBase", "HeygenAvatar", "SpriteAvatar", "persona_link_provider", "persona_link_providers" ]
