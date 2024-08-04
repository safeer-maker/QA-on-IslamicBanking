import os

__data_foulder = 'data'

__pdf_folder_name = 'pdf-data'
__zip_folder_name = 'zip-data'
__tmp_folder_name = "temp"
zip_file_name   = 'dir-lst.txt'
pdf_file_name   = 'dir-lst.txt'

pdf_folder = os.path.join (__data_foulder,__pdf_folder_name)
zip_folder = os.path.join (__data_foulder,__zip_folder_name)
tmp_folder = os.path.join (__data_foulder,__tmp_folder_name)
zip_file   = os.path.join (zip_folder,zip_file_name)
pdf_file   = os.path.join (pdf_folder,pdf_file_name)

print (os.system('pwd'))
print ("pdf_folder : ", pdf_folder )

db_foulder = 'vector_db'
collection_name = 'banking'
db_url = '0.0.0.0'
db_port = 8000

split_chunk = 500
split_overlap = 30




