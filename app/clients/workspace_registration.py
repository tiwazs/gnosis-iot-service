import os
import grpc
from grpc_gen.workspace.v1 import registration_pb2, registration_pb2_grpc

class WorkspaceRegistrationClient:
    def __init__(self, addr: str | None = None):
        self.addr = addr or os.getenv("WORKSPACE_GRPC_ADDR", "localhost:50051")

    async def redeem_token(self, token: str) -> registration_pb2.RedeemTokenResponse:
        async with grpc.aio.insecure_channel(self.addr) as channel:
            stub = registration_pb2_grpc.RegistrationServiceStub(channel)
            return await stub.RedeemToken(
                registration_pb2.RedeemTokenRequest(token=token)
            )