from pinecone.grpc import PineconeGRPC as Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

pc_api = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=pc_api)

print(pc.describe_index("fundybot"))