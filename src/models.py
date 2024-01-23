from typing import Final

import tm1637
from datetime import datetime
import time

from typing import Mapping,  Optional

from typing_extensions import Self

from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.utils import ValueTypes
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.components.generic import Generic

class TM1637(Generic):
    tm = None
    MODEL: Final = Model(ModelFamily("michaellee1019", "tm1637"), "time")

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        new_tm = cls(config.name)
        
        if 'clk_pin' in config.attributes.fields:
            clk = config.attributes.fields["clk_pin"].number_value
        if 'dio_pin' in config.attributes.fields:
            dio = config.attributes.fields["dio_pin"].number_value
        new_tm.tm = tm1637.TM1637(clk=int(clk), dio=int(dio))  # Using GPIO pins 18 and 17
        return new_tm

    @classmethod
    def validate_config(self, config: ComponentConfig) -> None:
        if 'clk_pin' not in config.attributes.fields or 'dio_pin' not in config.attributes.fields:
            raise Exception('clk_pin and dio_pin are required attributes of the TM1637 model')
        
        return None

    # Attributes example
    # {
    #     "clk_pin": 18,
    #     "dio_pin": 17
    # }    

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        result = {key: False for key in command.keys()}
        for (name, args) in command.items():
            if name == 'flash_time':
                self.flash_time(args['duration'])
                result[name] = True
        return result

    # Attributes example
    # {
    #     "flash_time": {"duration": 5},
    # }   

    def flash_time(self, duration: int):
        clear = [0, 0, 0, 0]  # Defining values used to clear the display
        self.tm.write(clear)
        now = datetime.now()
        hh = int(datetime.strftime(now,'%H'))
        mm = int(datetime.strftime(now,'%M'))
        self.tm.numbers(hh, mm, colon=True)
        time.sleep(duration)
        self.tm.write(clear)