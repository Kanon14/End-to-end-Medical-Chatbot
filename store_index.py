from src.helper import load_pdf_file, text_split, download_hf_embeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

#--------------------------------------------------
# Creating the Pinecone Index
#--------------------------------------------------
# Extract the data from the PDF file
extracted_data = load_pdf_file(data="data/")

# Split the data into chunks
text_chunks = text_split(extracted_data)

# Download the embedding model from HuggingFace
embeddings = download_hf_embeddings()

# Create the Pinecone index
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medicalbot"
pc.create_index(name=index_name, 
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"))

# Embed each chunk and upsert the embeddings to Pinecone Index
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks, 
    index_name=index_name,
    embedding=embeddings
)
