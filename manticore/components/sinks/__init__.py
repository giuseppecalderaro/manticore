### Factory
from manticore.components.sinks.sinks_factory import SinksFactory
from manticore.components.sinks.file_sink.file_sink import FileSink
from manticore.components.sinks.kafka_sink.kafka_sink import KafkaSink
from manticore.components.sinks.mock_sink.mock_sink import MockSink
from manticore.components.sinks.network_sink.network_sink import NetworkSink
from manticore.components.sinks.redis_sink.redis_sink import RedisSink

### File Sink
SinksFactory.register(FileSink)

### Kafka Sink
SinksFactory.register(KafkaSink)

### Mock Sink
SinksFactory.register(MockSink)

### Network Sink
SinksFactory.register(NetworkSink)

### Redis Sink
SinksFactory.register(RedisSink)
