import sys
from Module.Train import train
from Module.Eval import eval
import zipfile
import os
from FilesManager.FilesManager import FilesManager
from Utils.Logger import Logger
import urllib

if __name__ == "__main__":
    version_filename_flag = '.data_ver2'

    # create logger
    logger = Logger()

    application = sys.argv[1] if len(sys.argv) > 1 else None
    name = sys.argv[2] if len(sys.argv) > 2 else None
    gpu = sys.argv[3] if len(sys.argv) > 3 else None
    if application == "download":
        logger.log("Command: Download()")

        filesmanager = FilesManager()
        path = filesmanager.get_file_path("data.visual_genome.data")
        file_name = os.path.join(path, "data.zip")

        # Download Data
        logger.log("Download Data ...")
        url = "http://www.cs.tau.ac.il/~taunlp/scene_graph/data.zip"
        urllib.urlretrieve(url, file_name)

        # Extract data
        logger.log("Extract ZIP file ...")
        zip_ref = zipfile.ZipFile(file_name, 'r')
        zip_ref.extractall(path)
        zip_ref.close()

        # mark data version downloaded
        open(version_filename_flag, "wb").close()

    elif application == "eval":
        # check if requried data version downloaded
        if not os.path.isfile(version_filename_flag):
            print("Error: Data wasn't downloaded. Type python Run.py for instructions how to download\n\n")
            exit()    

        logger.log(f"Command: Eval(module_name={name}, gpu={str(gpu)}")
        eval(load_module_name=name, gpu=gpu)

    elif application == "train":
        # check if requried data version downloaded
        if not os.path.isfile(version_filename_flag):
            print("Error: Data wasn't downloaded. Type python Run.py for instructions how to download\n\n")
            exit()
        logger.log(f"Command: Train(module_name={name}, gpu={str(gpu)}")
        train(name=name, gpu=gpu)

    else:
        # print usage
        print("Error: unexpected usage\n\n")
        print("SGP Runner")
        print("----------")
        print("Download data: \"python Run.py download\"")
        print("               Should be run just once, on the first time the module used")
        print("Train Module: \"python Run.py train <module_name> <gpu_number>\"")
        print("               Train lingustic SGP")
        print("               Module weights with the highest score over the validation set will be saved as \"<module_name>_best\"")
        print("               Module weights of the last epoch will be saved as \"<module_name>\"")
        print("Eval Module: \"python Run.py eval <module_name> <gpu_number>\"")
        print("               Scene graph classification (recall@100) evaluation for the trained module.")
        print("               Use 'gpi_ling_orig_best' for a pre-trained module")
        print("               Use \"<module_name>_best\" for a self-trained module")
