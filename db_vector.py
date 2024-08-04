import chromadb
from chromadb.utils import embedding_functions
import config
from data_preperation import data_preperation
from data_extraction import data_extraction


class vector_db (data_preperation):
    def __init__ (self):
        super().__init__()
        # self.data = super().data_prep_pipeline()
        # self.vector_db = chromadb.PersistentClient (path=config.db_foulder)
        self.vector_db = chromadb.HttpClient (host=config.db_url, port=config.db_port)
        self.embeddings = embedding_functions.ONNXMiniLM_L6_V2()
        self.collection = self.vector_db.get_or_create_collection ( config.colelction_name , embedding_function=self.embeddings)
        
    def db_add (self, dict = {} ):

        if dict == {}:
            dict = super().data_prep_pipeline()
        # print (dict)
        collection = self.collection
        count = collection.count() 
        dic_len_pc = len(dict['page_content'])
        dic_len_md = len(dict['metadata'])
        
        if dic_len_pc == dic_len_md and dic_len_pc > 0:
            ids = [ str(i) for i in range(count, count + dic_len_md ) ]
            # print ("ids:",ids)
            print ("Adding data to database Please be patient. It will take some time".upper())
            collection.add(
                ids=ids,
                documents =dict['page_content'],
                metadatas=dict['metadata']
            )

        print( "count by  : ", collection.count())
        return 0

    def db_query(self, query):
        result = self.collection.query (query_texts= query)
        return result

    def db_del (self):
        self.vector_db.delete_collection(config.colelction_name)
        super().def_pdf_list()
        super().def_zip_list()
        # self.vector_db.reset()

    def db_extract_add (self):
        super().extraction_pipeline()
        self.db_add()


if __name__ == '__main__':
    cls = vector_db()

    # cls.db_add()
    # cls.db_del()
    cls.db_extract_add()
    print (cls.db_query("what is banking"))

