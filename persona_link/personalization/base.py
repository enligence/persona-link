"""
TODO: Use LLMs, or train a small LLM or model to take 
text, name and role as input and generate prefix / suffix personalization
text that can be play before or after the main message.
"""

from abc import ABC, abstractmethod

from persona_link.personalization.models import Personalization


class PersonalizationBase(ABC):
    @abstractmethod
    async def personalize(self, text: str, name: str, role: str=None) -> Personalization:
        """
        Based upon the settings provided, 
        the personalization will generate prefix and suffix text
        to be played before and after the main message.
        """
        pass