from google import genai
from redis_db import redis_client
import time
import tiktoken
# from pinecone import Pinecone # type: ignore
from db import conn
from config import GEMINI_API_KEY

client = genai.Client(
    api_key=GEMINI_API_KEY
)

# cursor = conn.cursor()

encoding = tiktoken.get_encoding(
    "cl100k_base"
)

personality = (
    "You are StormBreaker AI, inspired by Thor, God of Thunder. "
    "Speak confidently, humorously, and heroically. "
    "Keep responses entertaining and powerful. "
    "Occasionally use Marvel-style expressions naturally. "
    "If the answer include number then give it in number form not in alphabetical form"
    "Every response should include helpful and intelligent answers.\n" \
)

selected_model = "gemini-3.5-flash"


def text_to_embedding(text):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return response.embeddings[0].values[:1536]

def ask_stormbreaker(
    user_input,
    user_id,
    chat_id
    ):

    start_time = time.time()

    redis_key = f"chat:{chat_id}:recent_chat"
    recent_chat = redis_client.lrange(redis_key, 0, -1)
    recent_context = "\n".join(recent_chat)

    
    input_tokens = len(
        encoding.encode(user_input)
    )

    # with conn.cursor() as cursor:
    
        # cursor.execute(
        #     """
        #     SELECT conversation
        #     FROM memories
        #     WHERE user_id = %s
        #     AND type = 'conversation'
        #     ORDER BY embedding <=> %s::vector
        #     LIMIT 3
        #     """,
        #     (
        #         user_id,
        #         vector_str
        #     )
        # )

        # results = cursor.fetchall()


        # print(f"Memory Search : {time.time() - start_time}")
        
    #     cursor.execute(
    #         """
    #         SELECT document_text
    #         FROM memories
    #         WHERE type = 'document'
    #         ORDER BY embedding <=> %s::vector
    #         LIMIT 3
    #         """,
    #         (vector_str,)
    #     )

    #     pdf_results = cursor.fetchall()

    pdf_content = ""

    embedding = text_to_embedding(user_input)
    vector_str = "[" + ",".join(map(str, embedding)) + "]"
    print(f"Embedding : {time.time() - start_time}")

    with conn.cursor() as cursor:

        cursor.execute(
            """
            SELECT document_text
            FROM memories
            WHERE type='document'
            ORDER BY embedding <=> %s::vector
            LIMIT 3
            """,
            (vector_str,)
        )

        pdf_results = cursor.fetchall()

    for row in pdf_results:
        if row[0]:
            pdf_content += row[0] + "\n"

    # memory = ""

    # for row in results:
    #     if row[0]:
    #         memory += row[0] + "\n"

    enhanced_input = f"""
        Recent Conversation:
        {recent_context}

        Relevant PDF Chunks:
        {pdf_content}

        Current Question:
        {user_input}

        Instructions:
        - Use the recent conversation to maintain context.
        - If the PDF chunks contain information relevant to the question, use them.
        - If the PDF chunks are not relevant, ignore them completely.
        - If the answer is not in the PDF, rely on your own knowledge.
        - Always answer as StormBreaker AI.
        """

    response = client.models.generate_content(
        model=selected_model,
        contents=(
            f"{personality}\n\n"
            f"{enhanced_input}"
        )
    )

    print(f"Gemini : {time.time() - start_time}")

    response_text = response.text

    redis_client.rpush(redis_key,f"User: {user_input}")
    redis_client.rpush(redis_key,f"StormBreaker: {response_text}")
    redis_client.ltrim(redis_key,-20,-1)
    redis_client.expire(redis_key,86400)

    # conversation_text = f"""
    # User: {user_input}

    # StormBreaker:
    # {response_text}
    # """

    # conversation_embedding = text_to_embedding(conversation_text)
    # vector_str_conv = "[" + ",".join(map(str, conversation_embedding)) + "]"

    # with conn.cursor() as cursor:
    #     cursor.execute(
    #     """
    #         INSERT INTO memories
    #         (
    #             id,
    #             user_id,
    #             type,
    #             conversation,
    #             embedding
    #         )
    #         VALUES
    #         (
    #             %s,
    #             %s,
    #             %s,
    #             %s,
    #             %s
    #         )
    #         """,
    #         (
    #             str(uuid.uuid4()),
    #             user_id,
    #             "conversation",
    #             conversation_text,
    #             vector_str_conv
    #         )
    #     )

    #     conn.commit()

    output_tokens = len(
        encoding.encode(response_text)
    )

    print(f"Total : {time.time() - start_time}")

    print("One response cycle completed\n")

    return {
        "response": response_text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": (
            input_tokens +
            output_tokens
        )
    }