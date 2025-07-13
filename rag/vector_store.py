import os
import sys
import django
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment to access models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edurag.settings")
django.setup()

from core.models import Lesson


def build_vector_store():
    # create metadata from all the content from db
    contents = Lesson.objects.all()
    texts = [c.content for c in contents]
    metadata = [{"title": c.title, "grade": c.grade} for c in contents]

    # Split content
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.create_documents(texts, metadatas=metadata)

    # Embed with HuggingFace
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embedding)
    vectorstore.save_local("vector_index")


# directly run build_vector_store to create vector index
# of provided content
if __name__ == '__main__':
    build_vector_store()
