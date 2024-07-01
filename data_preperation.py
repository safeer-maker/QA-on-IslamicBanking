from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from data_extraction import data_extraction
import os
import config

class data_preperation (data_extraction):
    def __init__ (self):
        super().__init__()
        self.pdf_list = []
        self.pdf_document = []
        self.processed_document = []
        self.proc_doc_dict = {}

    def pdf_files_to_read (self, foulder_path_pdf = None):
        
        if foulder_path_pdf is None:
            foulder_path_pdf = config.pdf_folder

        pdf_files = os.listdir (foulder_path_pdf)

        if config.pdf_file_name in os.listdir (foulder_path_pdf):
            print (f"{config.pdf_file_name} file found")
        else:
            print (f"{config.pdf_file_name} NOT file found")
            # create a emplty file if file not exists
            with open (config.pdf_file, 'w' ) as x:
                pass
        
        pdf_precessed = []
        with open ( config.pdf_file , 'rt' ) as x:
            pdf_precessed = x.read ().split('\n')
            print ("files ", pdf_precessed)

        for file in pdf_files:
            if file not in pdf_precessed and file[-3:] == 'pdf':
                print (f"{file} is ready for Processing")
                self.pdf_list.append (file)

        return self.pdf_list
    
    def read_pdf (self, pdf_foulder = None):

        if pdf_foulder is None:
            pdf_foulder = config.pdf_folder

        for i in self.pdf_list:
            pdf_file = os.path.join (pdf_foulder, i)
            print (f"Reading {pdf_file}")
            pdf_document  = PyPDFLoader(pdf_file).load()
            self.pdf_document.extend(pdf_document)
            print (f"Read {pdf_file}")

            with open ( config.pdf_file  , "a+t" ) as file:
                    file.write ( i +'\n' )
        
        return self.pdf_document

    def split_doc (self, lst = []):
        if lst == []:
            lst = self.pdf_document

        splitter = RecursiveCharacterTextSplitter(
            chunk_size = config.split_chunk,
            chunk_overlap = config.split_overlap
        )

        split_doc = splitter.split_documents (lst)

        page_content = [ ]
        metadata = [ ]
        for doc in split_doc:
            page_content.append ( " ".join(str (doc.page_content).lower().split()))
            metadata.append     (doc.metadata)
        
        self.proc_doc_dict = {
            'page_content' : page_content,
            'metadata' : metadata
        }

        return self.proc_doc_dict
    
    def data_prep_pipeline (self):
        self.pdf_files_to_read()
        self.read_pdf()
        self.split_doc()
        return self.proc_doc_dict
    
    def def_pdf_list (self, path = None):
        if path is None:
            path = config.pdf_file 
        print ("deleting file at : ",path)
        with open ( path ,'wt') as w:
            pass
        return 0
    
    def delete_all_data(self, path = None):
        
        if path is None:
            path = config.pdf_folder 
    
        files = self.dir_ls =  os.listdir (path)
        file_path = [ os.path.join (path, file)  for file in files ]

        print (file_path)
        try:
            for files in file_path:
                 os.remove (files)
            with open ( config.pdf_file  ,'wt') as w:
                pass
            return 0
        except:
            print("An exception occurred")
            return -1
    
    def data_prep_pipeline (self):
        self.pdf_files_to_read()
        self.read_pdf()
        self.split_doc()

        #### temp
        # self.def_pdf_list()
        return self.proc_doc_dict
        

if __name__ == '__main__':
    cls = data_preperation()
    # cls.pdf_files_to_read()
    # print( cls.read_pdf() )
    # cls.split_doc()
    # cls.def_pdf_list()
    # cls.delete_all_data()
    print (cls.data_prep_pipeline())
