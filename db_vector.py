import chromadb
from chromadb.utils import embedding_functions
import config
from data_preperation import data_preperation
from data_extraction import data_extraction


class vector_db (data_preperation):
    def __init__(self):
        super().__init__()
        self.data = super().data_prep_pipeline()
        self.vector_db = chromadb.PersistentClient (path=config.db_foulder)
        self.embeddings = embedding_functions.ONNXMiniLM_L6_V2()
        self.collection = self.vector_db.get_or_create_collection ( config.colelction_name , embedding_function=self.embeddings)

    def db_add (self ):
        dict = self.data
        print (dict)
        collection = self.collection
        count = collection.count() 

        print (count , len(dict['page_content']))
        
        ids = [ str(i) for i in range(count, count + len(dict['page_content']))]
        print ("ids:",ids)
        collection.add(
            ids=ids,
            documents =dict['page_content'],
            metadatas=dict['metadata']
        )

        print(collection.count)
        

if __name__ == '__main__':
    cls = vector_db()

    cls.db_add()

