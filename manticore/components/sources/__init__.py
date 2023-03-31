### Factory
from manticore.components.sources.sources_factory import SourcesFactory
from manticore.components.sources.file_source.file_source import FileSource
from manticore.components.sources.kafka_source.kafka_source import KafkaSource
from manticore.components.sources.mock_source.mock_source import MockSource
from manticore.components.sources.network_source.network_source import NetworkSource
from manticore.components.sources.redis_source.redis_source import RedisSource

### File Source
SourcesFactory.register(FileSource)

### Kafka Source
SourcesFactory.register(KafkaSource)

### Mock Source
SourcesFactory.register(MockSource)

### Network Source
SourcesFactory.register(NetworkSource)

### Redis Source
SourcesFactory.register(RedisSource)
