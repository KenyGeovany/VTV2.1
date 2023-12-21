from class_path import path

path = path()

# Update test history
def update_test_history(message):
    f = open(path.TEST_HISTORY_TXT, "a")
    f.write(message)
    f.close()

# Update upload history
def update_upload_history(message):
    f = open(path.UPLOAD_HISTORY_TXT, "a")
    f.write(message)
    f.close()

# Update download history
def update_download_history(message):
    f = open(path.DOWNLOAD_HISTORY_TXT, "a")
    f.write(message)
    f.close()

# Update the test_exp
def update_test_exp(message):
    f = open(path.TEST_EXP_TXT, "a")
    f.write(message)
    f.close()

# Update the update_exp
def update_upload_exp(message):
    f = open(path.UPLOAD_EXP_TXT, "a")
    f.write(message)
    f.close()

# Update the download_exp
def update_download_exp(message):
    f = open(path.DOWNLOAD_EXP_TXT, "a")
    f.write(message)
    f.close()
