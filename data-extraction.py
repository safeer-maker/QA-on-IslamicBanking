import os
import config
import zipfile
import rarfile


class data_extraction ():
    def __init__ (self):
        self.dir_ls = []
        self.zip_filename = []
        self.un_zippded_filesname = []

    def read_all_zip_files (self, path = config.zip_folder):

        self.dir_ls =  os.listdir (path )

        # checking if the file lising all extracted zip exist
        # if not then make that file
        if "dir-lst.txt" in os.listdir (path):
            print ("dir-lst.txt file found")
        else:
            print ("dir-lst.txt NOT file found")
            # create a emplty file if file not exists
            with open ( os.path.join ( path , 'dir-lst.txt' ), 'w' ) as x:
                pass
        
        # reading all the names of files that are aleady extracted
        with open ( os.path.join ( path , 'dir-lst.txt' ) , 'rt' ) as x:
            self.un_zippded_filesname = x.read ().split('\n')
            print ("files ", self.un_zippded_filesname)

        # making a list of zip files that needed to be extracted
        for file in self.dir_ls:
            # zip_filenames.append ( if file in un_zippded_filesname : file )
            if file not in self.un_zippded_filesname and (file[-3:] == 'rar' or file[-3:] == 'zip'):
                print (f"{file} is ready for extraction")
                self.zip_filename.append (file)

        return 0

    def extract_files (self, path_to_extrect = config.pdf_folder):

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

            with open ( os.path.join ( config.zip_folder, 'dir-lst.txt'), "a+t" ) as file:
                    file.write ( i +'\n' )

        return 0    
    

if __name__ == '__main__':
    cls = data_extraction()
    cls.read_all_zip_files()

    print (cls.zip_filename)

    cls.extract_files()



