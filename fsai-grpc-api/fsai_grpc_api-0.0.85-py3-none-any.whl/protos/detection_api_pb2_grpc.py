# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from fsai_grpc_api.protos import detection_api_pb2 as fsai__grpc__api_dot_protos_dot_detection__api__pb2


class DetectionApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.FindOrCreateDetection = channel.unary_unary(
                '/DetectionApi/FindOrCreateDetection',
                request_serializer=fsai__grpc__api_dot_protos_dot_detection__api__pb2.DetectionRequest.SerializeToString,
                response_deserializer=fsai__grpc__api_dot_protos_dot_detection__api__pb2.DetectionResponse.FromString,
                )


class DetectionApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def FindOrCreateDetection(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DetectionApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'FindOrCreateDetection': grpc.unary_unary_rpc_method_handler(
                    servicer.FindOrCreateDetection,
                    request_deserializer=fsai__grpc__api_dot_protos_dot_detection__api__pb2.DetectionRequest.FromString,
                    response_serializer=fsai__grpc__api_dot_protos_dot_detection__api__pb2.DetectionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'DetectionApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DetectionApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def FindOrCreateDetection(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/DetectionApi/FindOrCreateDetection',
            fsai__grpc__api_dot_protos_dot_detection__api__pb2.DetectionRequest.SerializeToString,
            fsai__grpc__api_dot_protos_dot_detection__api__pb2.DetectionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
