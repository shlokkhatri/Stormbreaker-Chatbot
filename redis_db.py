import redis # type: ignore

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

try:
    redis_client.ping()
    print("Redis Connected")
except Exception as e:
    print("Redis Error:", e)