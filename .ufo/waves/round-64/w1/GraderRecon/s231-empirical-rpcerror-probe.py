import grpc, sys
# mirrors the grader's leg-6/leg-7 shape for a case whose server is NOT running:
# unary SetVal over an insecure channel to a closed loopback port.
print("grpc", grpc.__version__)
channel = grpc.insecure_channel("127.0.0.1:5329")
stub_like = channel.unary_unary("/KVStore/SetVal")
try:
    stub_like(b"x", timeout=5.0)
    print("RESULT: returned normally (unexpected)")
except grpc.RpcError as e:
    print("CAUGHT_AS_grpc_RpcError:", type(e).__name__)
    print("isinstance_RpcError:", isinstance(e, grpc.RpcError))
    print("code:", e.code(), "| code_is_UNAVAILABLE:", e.code() == grpc.StatusCode.UNAVAILABLE)
    print("details:", e.details())
finally:
    channel.close()
