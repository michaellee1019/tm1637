import asyncio

from viam.components.generic import Generic
from viam.module.module import Module
from viam.resource.registry import Registry, ResourceCreatorRegistration
from models import TM1637


async def main():
    """
    This function creates and starts a new module, after adding all desired
    resource models. Resource creators must be registered to the resource
    registry before the module adds the resource model.
    """
    Registry.register_resource_creator(
        Generic.SUBTYPE,
        TM1637.MODEL,
        ResourceCreatorRegistration(TM1637.new, TM1637.validate_config))
    module = Module.from_args()

    module.add_model_from_registry(Generic.SUBTYPE, TM1637.MODEL)
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())