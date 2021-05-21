# Authors:  Marcus Lönnqvist (maln1801) & Axel Hansson (axha1801)
# Desc:     A program that tests the compressibility of files. It uses 3 algorithms for testing.
# Version:  0.4

from tkinter import *
from tkinter import filedialog
import tkinter as tk
import os

root = Tk()
root.geometry("700x560")
root.title("Compression test program")

files_to_compress = []

# Creates textbox for file location
read_only_text = tk.Text(root, height=1, width=60)
read_only_text.insert(tk.END, "No files selected")
read_only_text.grid(row=0, column=0)

# Creates textbox for result details
details_text = tk.Text(root, height=30, width=60)
details_text.insert(tk.END, "Start the compression to see details")
details_text.grid(row=1, column=0)

# Creates radiobuttons for algorithm choice
algo_choice = StringVar()
label = Label()

R1 = Radiobutton(label, text="lzma", variable=algo_choice, value="lzma")
R1.pack(anchor=W)
R2 = Radiobutton(label, text="gzip", variable=algo_choice, value="gzip")
R2.pack(anchor=W)
R3 = Radiobutton(label, text="bz2", variable=algo_choice, value="bz2")
R3.pack(anchor=W)
R4 = Radiobutton(label, text="All algorithms", variable=algo_choice, value="all")
R4.pack(anchor=W)

R4.select()


# Changes the value of the read only textbox
def set_readonly_box(value):
    read_only_text.delete("1.0", END)
    read_only_text.insert(END, value)


# Changes the value of the detail textbox
def set_detail_box(value):
    details_text.delete(1.0, END)
    details_text.insert(END, value)


# Prompts user to choose dir to compress filesin
def opendir():
    global files_to_compress
    mapp = filedialog.askdirectory(parent=root, title="Choose a dir")
    for rootdir, dirs, files in os.walk(mapp):
        for file in files:
            if file.endswith(".java"):
                print("adding: " + file)
                files_to_compress.append(os.path.join(rootdir, file))

    set_readonly_box("Found " + str(len(files_to_compress)) + " files")


# Prompts user to choose files to compress
def openfile():
    global files_to_compress
    files_to_compress = filedialog.askopenfilenames(parent=root, title='Choose a file or files')
    set_readonly_box("Found " + str(len(files_to_compress)) + " files")


def compress_test(compress_type, file):

    # If there is no filepath, return
    if file is None:
        print("NO FILEPATH")
        return None

    print("Filepath: " + file)
    data_in = open(file, "rb")
    data = data_in.read()
    compressed_data = 0

    if compress_type == "lzma":
        import lzma
        compressed_data = lzma.compress(data, preset=lzma.PRESET_EXTREME)
    elif compress_type == "gzip":
        import gzip
        compressed_data = gzip.compress(data, compresslevel=9)
    elif compress_type == "bz2":
        import bz2
        compressed_data = bz2.compress(data, compresslevel=9)

    # Saves data size before compression and after
    data_size = data.__sizeof__()
    compressed_size = compressed_data.__sizeof__()

    compress_percent = (1 - (compressed_size / data_size)) * 100

    # Returns both string and compression percentage
    return [compress_percent, data_size, compressed_size]


def run_compress():
    # Saves all test records in lists
    lzma_list = []
    gzip_list = []
    bz2_list = []

    if algo_choice.get() == "all":
        for x in files_to_compress:
            lzma_list.append(compress_test("lzma", x))
            gzip_list.append(compress_test("gzip", x))
            bz2_list.append(compress_test("bz2", x))

    elif algo_choice.get() == "lzma":
        for x in files_to_compress:
            lzma_list.append(compress_test("lzma", x))

    elif algo_choice.get() == "gzip":
        for x in files_to_compress:
            gzip_list.append(compress_test("gzip", x))

    elif algo_choice.get() == "bz2":
        for x in files_to_compress:
            bz2_list.append(compress_test("bz2", x))

    # Calculates average compression rate
    lzma_percentage_sum = 0
    gzip_percentage_sum = 0
    bz2_percentage_sum = 0
    lzma_uncompressed_sum = 0
    gzip_uncompressed_sum = 0
    bz2_uncompressed_sum = 0
    lzma_compressed_sum = 0
    gzip_compressed_sum = 0
    bz2_compressed_sum = 0
    lzma_average = 0
    gzip_average = 0
    bz2_average = 0

    # Summing up the compression stats
    for x in lzma_list:
        lzma_percentage_sum += x[0]
        lzma_uncompressed_sum += x[1]
        lzma_compressed_sum += x[2]
    for x in gzip_list:
        gzip_percentage_sum += x[0]
        gzip_uncompressed_sum += x[1]
        gzip_compressed_sum += x[2]
    for x in bz2_list:
        bz2_percentage_sum += x[0]
        bz2_uncompressed_sum += x[1]
        bz2_compressed_sum += x[2]

    # Calculating average
    if algo_choice.get() == "gzip":
        gzip_average = gzip_percentage_sum / len(gzip_list)
        uncompressed_sum = gzip_uncompressed_sum
    elif algo_choice.get() == "bz2":
        bz2_average = bz2_percentage_sum / len(bz2_list)
        uncompressed_sum = bz2_uncompressed_sum
    elif algo_choice.get() == "lzma":
        lzma_average = lzma_percentage_sum / len(lzma_list)
        uncompressed_sum = lzma_uncompressed_sum
    else:
        uncompressed_sum = lzma_uncompressed_sum
        gzip_average = gzip_percentage_sum / len(gzip_list)
        bz2_average = bz2_percentage_sum / len(bz2_list)
        lzma_average = lzma_percentage_sum / len(lzma_list)

    average = 0
    if algo_choice.get() == "all":
        average = (lzma_average + gzip_average + bz2_average) / 3

    # Saving a string of things to print
    detail_string = "Uncompressed Size: " + str(uncompressed_sum) + " bytes"
    if algo_choice.get() == "lzma" or algo_choice.get() == "all":
        detail_string += "\n\nlzma compressed size: " + str(lzma_compressed_sum) + " bytes (" + str(lzma_average) + "%)"
    if algo_choice.get() == "gzip" or algo_choice.get() == "all":
        detail_string += "\ngzip compressed size: " + str(gzip_compressed_sum) + " bytes (" + str(gzip_average) + "%)"
    if algo_choice.get() == "bz2" or algo_choice.get() == "all":
        detail_string += "\nbz2 compressed size: " + str(bz2_compressed_sum) + " bytes (" + str(bz2_average) + "%)"
    if algo_choice.get() == "all":
        detail_string += "\n\nAverage compression rate: " + str(average) + "%"

    # Prints info in details box
    set_detail_box(detail_string)


def run_serial():
    # Saves all test records in lists
    lzma_list = []
    gzip_list = []
    bz2_list = []

    if algo_choice.get() == "all":
        for x in files_to_compress:
            lzma_list.append(compress_test("lzma", x))
            gzip_list.append(compress_test("gzip", x))
            bz2_list.append(compress_test("bz2", x))

    elif algo_choice.get() == "lzma":
        for x in files_to_compress:
            lzma_list.append(compress_test("lzma", x))

    elif algo_choice.get() == "gzip":
        for x in files_to_compress:
            gzip_list.append(compress_test("gzip", x))

    elif algo_choice.get() == "bz2":
        for x in files_to_compress:
            bz2_list.append(compress_test("bz2", x))

    detail_string = ""

    if algo_choice.get() == "all":
        for i in range(len(lzma_list)):
            average = (lzma_list[i][0] + gzip_list[i][0] + bz2_list[i][0]) / 3

            # Saving a string of things to print
            detail_string += "Filename: " + str(files_to_compress[i]) \
                            + "\nUncompressed Size: " + str(lzma_list[i][1]) + " bytes" \
                            + "\n\nlzma compressed size: " + str(lzma_list[i][2]) \
                            + " bytes (" + str(lzma_list[i][0]) + "%)" \
                            + "\ngzip compressed size: " + str(gzip_list[i][2]) + " bytes (" + str(gzip_list[i][0]) + "%)" \
                            + "\nbz2 compressed size: " + str(bz2_list[i][2]) + " bytes (" + str(bz2_list[i][0]) + "%)" \
                            + "\n\nAverage compression rate: " + str(average) + "%\n\n\n\n"

    elif algo_choice.get() == "lzma":
        for i in range(len(lzma_list)):
            # Saving a string of things to print
            detail_string += "Filename: " + str(files_to_compress[i]) \
                             + "\nUncompressed Size: " + str(lzma_list[i][1]) + " bytes" \
                             + "\n\nlzma compressed size: " + str(lzma_list[i][2]) \
                             + " bytes (" + str(lzma_list[i][0]) + "%)\n\n\n\n"

    elif algo_choice.get() == "gzip":
        for i in range(len(gzip_list)):
            # Saving a string of things to print
            detail_string += "Filename: " + str(files_to_compress[i]) \
                             + "\nUncompressed Size: " + str(gzip_list[i][1]) + " bytes" \
                             + "\ngzip compressed size: " + str(gzip_list[i][2]) + " bytes (" + str(gzip_list[i][0]) + \
                             "%)\n\n\n\n"

    elif algo_choice.get() == "bz2":
        for i in range(len(bz2_list)):
            # Saving a string of things to print
            detail_string += "Filename: " + str(files_to_compress[i]) \
                             + "\nUncompressed Size: " + str(bz2_list[i][1]) + " bytes" \
                             + "\nbz2 compressed size: " + str(bz2_list[i][2]) + " bytes (" + str(bz2_list[i][0]) + \
                             "%)\n\n\n\n"

    # Prints info in details box
    set_detail_box(detail_string)


# Creates button to choose file
button_open_dir = Button(root, text="Open Directory", fg="black", command=opendir)
button_open_dir.grid(row=0, column=2)
button_open_file = Button(root, text="Open File", fg="black", command=openfile)
button_open_file.grid(row=0, column=1)

# Adds radiobutton for algorithm choice
label.grid(row=1, column=1)

# Creates button to start compression
button_compress = Button(root, text="Start Compression", fg="black", command=run_compress)
button_compress.grid(row=2, column=1)
button_serial_compress = Button(root, text="Start Serialized", fg="black", command=run_serial)
button_serial_compress.grid(row=2, column=2)

root.mainloop()
