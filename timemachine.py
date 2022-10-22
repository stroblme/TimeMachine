import os
from pathlib import Path

from hachoir.parser import createParser
from hachoir.editor import createEditor
from hachoir.field import writeIntoFile
from hachoir.metadata import extractMetadata


GLOBPATTERN = "**/*.MOV"


def timewarp(fileinput, fileoutput, dt_year=0, dt_month=0, dt_day=0, dt_hour=0, dt_min=0, dt_sec=0):
    parser = createParser(fileinput)
    with parser:
        editor = createEditor(parser)
        creation_date = editor['/atom[2]/movie/atom[0]/movie_hdr']["creation_date"].value
        editor['/atom[2]/movie/atom[0]/movie_hdr']["creation_date"].value = creation_date.replace(  year=creation_date.year+dt_year,
                                                                                                    month=creation_date.month+dt_month,
                                                                                                    day=creation_date.day+dt_day,
                                                                                                    hour=creation_date.hour+dt_hour,
                                                                                                    minute=creation_date.minute+dt_min,
                                                                                                    second=creation_date.second+dt_sec)

        lastmod_date = editor['/atom[2]/movie/atom[0]/movie_hdr']["lastmod_date"].value
        editor['/atom[2]/movie/atom[0]/movie_hdr']["lastmod_date"].value = lastmod_date.replace(    year=lastmod_date.year+dt_year,
                                                                                                    month=lastmod_date.month+dt_month,
                                                                                                    day=lastmod_date.day+dt_day,
                                                                                                    hour=lastmod_date.hour+dt_hour,
                                                                                                    minute=lastmod_date.minute+dt_min,
                                                                                                    second=lastmod_date.second+dt_sec)

        # metadata = extractMetadata(parser)
        writeIntoFile(editor, fileoutput)

def main():

    print("##### Timemachine #####\n")
    print("Press Ctrl-C if you did not created a backup so far or want to cancel at any point!")
    print("\nThis program will modify the creation and modification date of all *.MOV files in the provided folder.")
    print("\n##### ########### #####\n")
    ctd = False
    while not ctd:
        try:
            folder = input("\nFirst, enter a folder path (Enter to use current folder): \t")
        except KeyboardInterrupt:
            print("\n\nSorry to see you go!")
            return

        try:
            folder_path = Path(folder)
            ctd=True
        except Exception:
            print("Sorry, somehow I cannot understand the provided folder path. Please try again and make sure you give me an absolute path.")


        files = folder_path.glob(GLOBPATTERN)
        files_list = list(files)

        if len(files_list) == 0:
            print("\nThere are no files in this folder. Let's try again!")
            ctd=False
            continue

        print(f"\nI found {len(files_list)} files in the folder, among which are:")
        for i, f in enumerate(files_list):
            print(f)
            if i > 5:
                break

        try:
            input("\nDoes this look ok?")
        except KeyboardInterrupt:
            print("\nOk, let's try again.. (Ctrl-C again to quit)\n")
            ctd=False

    print("\nOk, lets get to the fun part. You are now being asked to specify the timeshift applied to each of your files. Please provide only integer values (optionally with '-' sign).")

    ctd=False
    while not ctd:
        try:
            dt_year = input("How many years do you want to travel? (Enter to skip year):\t")
            dt_month = input("How many months do you want to travel? (Enter to skip month):\t")
            dt_day = input("How many days do you want to travel? (Enter to skip day):\t")
            dt_hour = input("How many hours do you want to travel? (Enter to skip hour):\t")
            dt_min = input("How many minutes do you want to travel? (Enter to skip minute):\t")
            dt_sec = input("How many seconds do you want to travel? (Enter to skip second):\t")
        except KeyboardInterrupt:
            print("\n\nSorry to see you go!")
            return

        timeshift = [dt_year, dt_month, dt_day, dt_hour, dt_min, dt_sec]

        for i, dt in enumerate(timeshift):
            try:
                if dt == "":
                    timeshift[i] = 0
                else:
                    timeshift[i] = int(dt)
                ctd = True
            except Exception:
                print("Cannot parse {dt} to integer.")
                ctd = False
                break

    print(f"\nOk, now the timeshift looks like:\t {timeshift}\n(year, month, day, hour, minute, second)")

    try:
        input("\nIs that correct? Press any key to continue and I'll start processing your files.")
    except KeyboardInterrupt:
        print("\n\nSorry to see you go!")
        return

    for i, movie_path in enumerate(files_list):
        try:
            output_file = movie_path.with_name('mod_'+movie_path.name)
            timewarp(movie_path.as_posix(), output_file.as_posix(), *timeshift)
        except:
            print(f"Something went wrong wile processing file {movie_path}. Will continue..")

    print("I'm done! :)")

if __name__ == '__main__':
    main()