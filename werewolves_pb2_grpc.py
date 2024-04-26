# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import werewolves_pb2 as werewolves__pb2


class WerewolvesServiceStub(object):
    """The Werewolves service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Connect = channel.unary_unary(
                '/werewolves.WerewolvesService/Connect',
                request_serializer=werewolves__pb2.ConnectRequest.SerializeToString,
                response_deserializer=werewolves__pb2.ConnectResponse.FromString,
                )
        self.InteractiveMessage = channel.stream_stream(
                '/werewolves.WerewolvesService/InteractiveMessage',
                request_serializer=werewolves__pb2.MessageRequest.SerializeToString,
                response_deserializer=werewolves__pb2.MessageResponse.FromString,
                )
        self.StartGame = channel.unary_unary(
                '/werewolves.WerewolvesService/StartGame',
                request_serializer=werewolves__pb2.MessageRequest.SerializeToString,
                response_deserializer=werewolves__pb2.MessageResponse.FromString,
                )
        self.WerewolvesVote = channel.unary_unary(
                '/werewolves.WerewolvesService/WerewolvesVote',
                request_serializer=werewolves__pb2.MessageRequest.SerializeToString,
                response_deserializer=werewolves__pb2.MessageResponse.FromString,
                )
        self.TownsPeopleVote = channel.unary_unary(
                '/werewolves.WerewolvesService/TownsPeopleVote',
                request_serializer=werewolves__pb2.MessageRequest.SerializeToString,
                response_deserializer=werewolves__pb2.MessageResponse.FromString,
                )


class WerewolvesServiceServicer(object):
    """The Werewolves service definition.
    """

    def Connect(self, request, context):
        """Connects a user
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InteractiveMessage(self, request_iterator, context):
        """Stream messages to clients
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartGame(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def WerewolvesVote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def TownsPeopleVote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WerewolvesServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Connect': grpc.unary_unary_rpc_method_handler(
                    servicer.Connect,
                    request_deserializer=werewolves__pb2.ConnectRequest.FromString,
                    response_serializer=werewolves__pb2.ConnectResponse.SerializeToString,
            ),
            'InteractiveMessage': grpc.stream_stream_rpc_method_handler(
                    servicer.InteractiveMessage,
                    request_deserializer=werewolves__pb2.MessageRequest.FromString,
                    response_serializer=werewolves__pb2.MessageResponse.SerializeToString,
            ),
            'StartGame': grpc.unary_unary_rpc_method_handler(
                    servicer.StartGame,
                    request_deserializer=werewolves__pb2.MessageRequest.FromString,
                    response_serializer=werewolves__pb2.MessageResponse.SerializeToString,
            ),
            'WerewolvesVote': grpc.unary_unary_rpc_method_handler(
                    servicer.WerewolvesVote,
                    request_deserializer=werewolves__pb2.MessageRequest.FromString,
                    response_serializer=werewolves__pb2.MessageResponse.SerializeToString,
            ),
            'TownsPeopleVote': grpc.unary_unary_rpc_method_handler(
                    servicer.TownsPeopleVote,
                    request_deserializer=werewolves__pb2.MessageRequest.FromString,
                    response_serializer=werewolves__pb2.MessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'werewolves.WerewolvesService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WerewolvesService(object):
    """The Werewolves service definition.
    """

    @staticmethod
    def Connect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/werewolves.WerewolvesService/Connect',
            werewolves__pb2.ConnectRequest.SerializeToString,
            werewolves__pb2.ConnectResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InteractiveMessage(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/werewolves.WerewolvesService/InteractiveMessage',
            werewolves__pb2.MessageRequest.SerializeToString,
            werewolves__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StartGame(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/werewolves.WerewolvesService/StartGame',
            werewolves__pb2.MessageRequest.SerializeToString,
            werewolves__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def WerewolvesVote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/werewolves.WerewolvesService/WerewolvesVote',
            werewolves__pb2.MessageRequest.SerializeToString,
            werewolves__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def TownsPeopleVote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/werewolves.WerewolvesService/TownsPeopleVote',
            werewolves__pb2.MessageRequest.SerializeToString,
            werewolves__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
