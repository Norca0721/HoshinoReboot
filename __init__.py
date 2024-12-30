from hoshino import Service, priv
from hoshino.log import new_logger
from hoshino.config import NICKNAME, PORT


from pathlib import Path

log = new_logger('HoshinoReboot')
BOTNAME = NICKNAME if isinstance(NICKNAME, str) else list(NICKNAME)[0]
Port = PORT if isinstance(PORT, int) else list(PORT)[0]

SV_HELP = 'nothing'
sv = Service('HoshinoReboot', manage_priv=priv.SUPERUSER, enable_on_default=False, help_=SV_HELP, visible=False)

ROOT = Path(__file__).parent
SAMPLE = ROOT / 'data' / 'sample.json'