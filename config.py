import os

__data_foulder = 'data'

__pdf_folder_name = 'pdf-data'
__zip_folder_name = 'zip-data'
__tmp_folder_name = "temp"

pdf_folder = os.path.join (__data_foulder,__pdf_folder_name)
zip_folder = os.path.join (__data_foulder,__zip_folder_name)
tmp_folder = os.path.join (__data_foulder,__tmp_folder_name)

print ("pdf_folder : ", pdf_folder )


