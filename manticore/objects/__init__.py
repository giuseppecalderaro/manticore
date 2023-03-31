### Factory
from manticore.objects.objects_factory import ObjectsFactory
from manticore.objects.normalised.mock import MockV1, MockV2

### Mock object
ObjectsFactory.register(MockV1)
ObjectsFactory.register(MockV2)
