from enum import Enum
from typing import List

from pydantic import BaseModel


class Locale(Enum):
    # Major International Languages
    EN_US = 'en-US' # English, United States
    ZH_CN = 'zh-CN' # Chinese, China (Simplified)
    ES_ES = 'es-ES' # Spanish, Spain
    DE_DE = 'de-DE' # German, Germany
    HI_IN = 'hi-IN' # Hindi, India
    AR_SA = 'ar-SA' # Arabic, Saudi Arabia
    PT_BR = 'pt-BR' # Portuguese, Brazil
    RU_RU = 'ru-RU' # Russian, Russia
    FR_FR = 'fr-FR' # French, France
    TR_TR = 'tr-TR' # Turkish, Turkey
    IT_IT = 'it-IT' # Italian, Italy
    JA_JP = 'ja-JP' # Japanese, Japan
    KO_KR = 'ko-KR' # Korean, Korea

    # Major Indian Languages
    BN_IN = 'bn-IN' # Bengali, India
    TE_IN = 'te-IN' # Telugu, India
    MR_IN = 'mr-IN' # Marathi, India
    TA_IN = 'ta-IN' # Tamil, India
    UR_IN = 'ur-IN' # Urdu, India
    GU_IN = 'gu-IN' # Gujarati, India
    KN_IN = 'kn-IN' # Kannada, India
    ML_IN = 'ml-IN' # Malayalam, India
    OR_IN = 'or-IN' # Oriya, India
    PA_IN = 'pa-IN' # Punjabi, India
    
class Type(Enum):
    FIRSTNAME="name"
    FULLNAME="full_name"
    GREETING="greeting"
    VALEDICTION="valediction"
    PREFIX="prefix"
    SUFFIX="suffix"
    
class Personalization(BaseModel):
    Personalization_type: Type
    text: str
    locale: Locale = Locale.EN_US
    
    @classmethod
    def standard_greeting(cls) -> List['Personalization']:
        return [
            cls(Personalization_type=Type.GREETING, text="Hello,"),
            cls(Personalization_type=Type.GREETING, text="Hi"),
            cls(Personalization_type=Type.GREETING, text="Good morning"),
            cls(Personalization_type=Type.GREETING, text="Good afternoon"),
            cls(Personalization_type=Type.GREETING, text="Good evening"),
            
        ]
        
    @classmethod
    def standard_valediction(cls) -> List['Personalization']:
        return [
            cls(Personalization_type=Type.VALEDICTION, text="Goodbye"),
            cls(Personalization_type=Type.VALEDICTION, text="It was nice talking to you"),
            cls(Personalization_type=Type.VALEDICTION, text="See you later"),
            cls(Personalization_type=Type.VALEDICTION, text="Have a great day"),
        ]
        
    @classmethod
    def standard_filler(cls) -> List['Personalization']:
        return [
            cls(Personalization_type=Type.FILLER, text="um"),
            cls(Personalization_type=Type.FILLER, text="uh"),
            cls(Personalization_type=Type.FILLER, text="like"),
            cls(Personalization_type=Type.FILLER, text="you know"),
        ]