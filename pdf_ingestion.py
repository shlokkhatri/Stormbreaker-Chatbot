from pypdf import PdfReader #type: ignore
from chatbot_1 import text_to_embedding
from google.genai.errors import ClientError #type: ignore
from db import conn
import uuid
import time

reader = PdfReader("stormbreaker_info.pdf")

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"

chunks = []

chunk_size = 1000

for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])
    
print(f"Total Chunks : {len(chunks)}")

for i, chunk in enumerate(chunks):

    while True:

        try:

            print(
                f"Embedding Chunk {i + 1}/{len(chunks)}"
            )

            embedding = text_to_embedding(chunk)

            vector_str = "[" + ",".join(map(str, embedding)) + "]"

            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO memories
                    (
                        id,
                        type,
                        document_text,
                        embedding
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        str(uuid.uuid4()),
                        "document",
                        chunk,
                        vector_str
                    )
                )

                conn.commit()

            break

        except ClientError as e:

            if "429" in str(e):

                print(
                    "Rate limit hit. Waiting 30 seconds..."
                )

                time.sleep(30)

            else:
                raise

print("\nPDF Successfully Uploaded!")
print(f"Inserted {len(chunks)} chunks into PostgreSQL.")