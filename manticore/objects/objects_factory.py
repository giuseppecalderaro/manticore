from typing import Dict, Type
from manticore.interfaces.object import Object
from manticore.objects.generic_object import Package
# from manticore.utils.logger import Logger


class ObjectsFactory:
    __objects: Dict[str, Dict[int, Type[Object]]] = {}

    @staticmethod
    def register(obj: Type[Object]) -> None:
        # The logger is not initialised yet, we can not use it here
        if obj.get_type() not in ObjectsFactory.__objects:
            ObjectsFactory.__objects[obj.get_type()] = {}

        ObjectsFactory.__objects[obj.get_type()][obj.get_version()] = obj

    @staticmethod
    def make(obj_type: str, obj_version: int) -> Type[Object]:
        if obj_type in ObjectsFactory.__objects:
            ret = ObjectsFactory.__objects[obj_type][obj_version]
            # Logger().debug(f'ObjectsFactory: built {obj_type}')
            return ret

        raise RuntimeError(f'ObjectsFactory cannot build object type {obj_type}')


    @staticmethod
    def make_package(obj: Object, source: str, destination: str) -> Package:
        pkg = Package(obj.get_type(),
                      obj.get_version(),
                      source,
                      destination,
                      obj)
        return pkg
