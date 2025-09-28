from dataclasses import dataclass
from datetime import datetime
@dataclass
class Event:
    uid:str; title:str; start:datetime; end:datetime|None=None
