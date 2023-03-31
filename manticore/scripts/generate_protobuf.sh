#!/usr/bin/env bash

protoc -Imanticore/interfaces/protobuf --python_out=manticore/generated common.proto
protoc -Imanticore/interfaces/protobuf --python_out=manticore/generated messages.proto
# python -m grpc_tools.protoc -Iinterfaces/protobuf --python_out=generated --grpc_python_out=generated api.proto
