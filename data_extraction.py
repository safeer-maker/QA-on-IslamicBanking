import os
import config
import zipfile
import rarfile


class data_extraction ():
    def __init__ (self):
        self.dir_ls = []
        self.zip_filename = []
        self.un_zippded_filesname = []


    def read_all_zip_files (self, path = None):

        if path is None:
            path = config.zip_folder
    
        self.dir_ls =  os.listdir (path )

        # checking if the file lising all extracted zip exist
        # if not then make that file
        if config.zip_file_name in os.listdir (path):
            print (f"{config.zip_file_name} file found")
        else:
            print (f"{config.zip_file_name} NOT file found")
            # create a emplty file if file not exists
            with open (config.zip_file, 'w' ) as x:
                pass
        
        # reading all the names of files that are aleady extracted
        with open ( config.zip_file , 'rt' ) as x:
            self.un_zippded_filesname = x.read ().split('\n')
            print ("files ", self.un_zippded_filesname)

        # making a list of zip files that needed to be extracted
        for file in self.dir_ls:
            # zip_filenames.append ( if file in un_zippded_filesname : file )
            if file not in self.un_zippded_filesname and (file[-3:] == 'rar' or file[-3:] == 'zip'):
                print (f"{file} is ready for extraction")
                self.zip_filename.append (file)

        return self.zip_filename


    def extract_files (self, path_to_extrect = None):
        """ Dependensies
        pip install rarfile
        sudo apt-get install unrar
        """

        if path_to_extrect is None:
            path_to_extrect = config.pdf_folder
        # Lets extract those files

        for i in  self.zip_filename:

            compress_file = os.path.join( config.zip_folder , i )

            if compress_file.endswith (".zip"):
                with zipfile.ZipFile (compress_file, "r") as comp_zip:
                    comp_zip.extractall (path_to_extrect)
                    print ("Extraction sucessfull : ", compress_file)

            if compress_file.endswith ('.rar'):
                with rarfile.RarFile (compress_file, "r") as comp_rar:
                    comp_rar.extractall (path_to_extrect)
                    print ("Extraction sucessfull : ", compress_file)

            with open ( config.zip_file  , "a+t" ) as file:
                    file.write ( i +'\n' )

        return 0
    

    def delete_text_file (self, path = None):

        if path is None:
            path = config.zip_file 
        
        print ("deleting file at : ",path)

        with open ( path ,'wt') as w:
            pass

        return 0


    def delete_all_data(self, path = None):

        if path is None:
            path = config.zip_folder 
    
        files = self.dir_ls =  os.listdir (path)
        file_path = [ os.path.join (path, file)  for file in files ]

        print (file_path)
        try:
            for files in file_path:
                 os.remove (files)
            with open ( config.zip_file  ,'wt') as w:
                pass
            return 0
        except:
            print("An exception occurred")
            return -1

       
    def extraction_pipeline (self, foulder_path_zip = None, foulder_path_pdf = None ):
        if foulder_path_pdf  is None:
            foulder_path_pdf = config.pdf_folder
        if foulder_path_zip is None:
            foulder_path_zip = config.zip_folder

        try:
            self.read_all_zip_files(foulder_path_zip)
            self.extract_files(foulder_path_pdf)
            print ("\n\nextraction pipeline sucessfull\n\n")
        except:
            print ("\n\nextraction pipeline failed\n\n".upper())
            return-1


if __name__ == '__main__':
    cls = data_extraction()
    # cls.read_all_zip_files()
    # print (cls.zip_filename)

    # cls.extract_files()

    cls.delete_text_file()
    cls.delete_all_data ()
    cls.extraction_pipeline()

