import os
import requests
import threading


# foler empty test
def if_empty(folderPath):
    try:
        file_list = os.listdir(folderPath)
    except FileNotFoundError:
        print("Foleder {} Not Existing.".format(folderPath))

    if len(file_list) != 0:
        return True
    else:
        return False


# download picture & write to file
def downloader(fileName, fileContent):

    with open(fileName, "wb") as f:
        print("Downloading {}...".format(fileName))
        f.write(fileContent)


# get files in list in multi-threads
def multi_downloader(urlList, folderName):
    store_in = os.environ["HOMEPATH"] + "\\Pictures\\the6688\\" + folderName + "\\"

    if os.path.exists(store_in) and if_empty(store_in):
        print("Folder {} exists and there are files in it.".format(store_in))
        exit()
    else:
        os.mkdir(store_in)
        print("Folder {} created".format(store_in))

    os.chdir(store_in)  # change working dir there

    for i in range(len(urlList)):
        threading.Thread(target=downloader, args=(urlList[i].split("/")[-1], requests.get(urlList[i]).content,)).start()


if __name__ == "__main__":
    multi_downloader(["http://img10.biao12.com/uploadfiles/images/2016/11/21/20161121132557281.jpg", "http://img10.biao12.com/uploadfiles/images/2016/11/13/20161113233623750.jpg"], "HIHI")
