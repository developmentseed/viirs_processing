import sys, os
from os import path as op
import os, sys
op.dirname(sys.executable)
import wget
import tarfile
from multiprocessing import Process, Pipe

def wget_file(file_url, conn):
    try:
      wget.download(file_url)
      print("File {} downloaded!".format(file_url))
      conn.send([file_url])
      conn.close()
    except Exception as e:
      print('Got exception: {0}'.format(e))
      raise e

def process_pool(file_urls):
    # create a list to keep all processes
    processes = []

    # create a list to keep connections
    parent_connections = []

    # create a process per file
    for url in file_urls:
        # create a pipe for communication
        parent_conn, child_conn = Pipe()
        parent_connections.append(parent_conn)

        # create the process, pass rile and connection
        process = Process(target=wget_file, args=(url, child_conn))
        processes.append(process)

    # start all processes
    for process in processes:
        process.start()

    # make sure that all processes have finished
    for process in processes:
        process.join()

    files_total = 0
    for parent_connection in parent_connections:
        files_total += parent_connection.recv()[0]

    return files_total

def parallel_wget(host, path, files):
    file_urls = ['{0}{1}{2}'.format(host, path, f) for f in files]
    print('\n'.join(file_urls))
    print("Downloading files~")
    process_pool(file_urls)
    downloaded_files = [op.join(os.getcwd(), f) for f in os.listdir(".") if op.isfile(f)]
    for file in downloaded_files:
        if file.endswith(".tgz"):
            print("unziping {}".format(file))
            tar = tarfile.open(file, "r:gz")
            tar.extractall()
            tar.close()
            os.remove(file)
            print("{} has remove".format(file))
    print('Completed download of {0} files'.format(len(files)))
