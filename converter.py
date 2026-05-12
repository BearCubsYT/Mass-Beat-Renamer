from colorama import Fore, Back, Style
from pathlib import Path
import time
import string
import re
import os
from pydub import AudioSegment
import ffmpeg

print (Style.BRIGHT)

def folderChecker(folder):
    Path(folder + "\\Sorter").mkdir(exist_ok=True)
    Path(folder + "\\Finished Files").mkdir(exist_ok=True)
    for file in (list(Path(folder).iterdir())):
        try: 
            if str(file).endswith(".wav") or str(file).endswith(".mp3"):
                Path(file).move_into(folder + "\\Sorter")
        except:
            pass
        
def intro():
    print(Fore.BLUE + "Please input the FULL path to your folder of beats below:" + Fore.WHITE)
    folder = input("")

    print(Fore.GREEN + "Thank You!" + Fore.WHITE)
    folderChecker(folder)
    time.sleep(1)
    print("\n\n\n\n")
    return folder
    
def separatorFinder(fileName: str):
    if len(fileName.split("-")) > 2:
        separator = "-"
    elif len(fileName.split(".")) > 3:
        separator = "."
    elif len(fileName.split("·")) > 2:
        separator = "·"
    elif len(fileName.split("|")) > 2:
        separator = "|"
    else:
        print(Fore.RED + "\n UNABLE TO FIND A SECTION SEPARATOR, I.E. (\"-\", \".\", \"·\")\n PLEASE TYPE THE SEPARATOR CHARACTER" + Fore.WHITE)
        separator = input("Separator: ").strip()
    
    return separator

def fileRenamer(folder):
    for file in (list(Path(folder + "\\Sorter").iterdir())):
        fileName = str(file).split("\\")[len(str(file).split("\\")) - 1]
        print(Fore.BLUE + "Type the first letter of each \"type\" in order of the below file, if no answer for that type exists in the file name wrap the answer in parentheses! You should seperate each section with a period \n" + Fore.RED + "Producer: P\nBPM: B\nKey: K\nName: N\nTags: T\n" + Fore.GREEN + "Example: N.B.P.(A Sharp Minor).(Hard, Rage)")
        print(Fore.WHITE + fileName)
        order = input("\nOrder: ").split(".")
        separator = separatorFinder(fileName)
        if separator:
            sectionList = fileName.removesuffix(".wav").removesuffix(".mp3").split(separator)
            times = 0
            producers = None
            bpm = None
            key = None
            name = None
            tags = None
            for type in order:
                if type.lower() == "p":
                    producers = list(map(str.strip, re.sub(r'·', '+', re.sub(r',', '+', re.sub(r'(?<=[a-zA-Z0-9]) (?=[a-zA-Z0-9])', '+', re.sub(r'(?<= )X', '+', re.sub(r'(?<= )x', '+', sectionList[times].removeprefix("@")))))).split("+")))
                elif type.lower() == "b":
                    bpm = re.findall(r'\d+', sectionList[times])
                elif type.lower() == "k":
                    key = sectionList[times].strip().title()
                    if "#" in key:
                        key = key[0] + " Sharp " + key[-5:]
                elif type.lower() == "n":
                    name = sectionList[times].strip().title()
                elif type.lower() == "t":
                    tags = list(map(str.strip, re.sub(r'·', '+', re.sub(r',', '+', re.sub(r'(?<=[a-zA-Z0-9]) (?=[a-zA-Z0-9])', '+', re.sub(r'(?<= )x', '+', sectionList[times].removeprefix("(").removesuffix(")"))))).split("+")))
                elif "Minor" in type or "Major" in type:
                    key = type.removeprefix("(").removesuffix(")").title()
                else:
                    tags = type.removeprefix("(").removesuffix(")").title().split(",")
                    
                times += 1
            
            newFileName = ""
            times = 1
            for producer in producers:
                newFileName += ("@" + str(producer).title())
                if times < len(producers):
                    newFileName += " X "
                times += 1
            newFileName += (" - " + str(bpm).removeprefix("['").removesuffix("']") + "BPM" + " - " + str(key) + " - " + str(name) + " ")
            times = 1
            for tag in tags:
                newFileName += (tag.strip())
                if times < len(tags):
                    newFileName += ", "
                times += 1
            newFileName += ")"
            print(Fore.GREEN + "\nIs this correct? (Y/N)\n" + Fore.BLUE + newFileName)
            answer = input(Fore.WHITE + "Answer: ")

            if answer.lower() == "y":
                print(Fore.GREEN + "Good!" + Fore.WHITE)
                time.sleep(1)
                print("\n\n\n\n")
            else:
                print(Fore.RED + "I'm sorry to hear that, send me a DM containing the name of the beat and I will try to update the app with an exception for names like this one!")
                print("You can manually type the beat name below")
                newFileName = input("Name: ")
                time.sleep(1)
                print("\n\n\n\n")
            
        else:
            print(Fore.RED + "UNABLE TO SPLIT THE SECTIONS, MUST BE DONE MANUALLY, PLEASE TYPE THE NEW FILE NAME (NOT INCLUDING THE FILE EXTENSION)" + Fore.WHITE)
            newFileName = input("New File Name: ")

        Path(folder + "\\Finished Files\\" + newFileName).mkdir(exist_ok=True)
        Path(folder + "\\Sorter\\" + fileName).move_into(folder + "\\Finished Files\\" + newFileName)
        if str(file).endswith(".wav"):
            os.rename(folder + "\\Finished Files\\" + newFileName + "\\" + fileName, folder + "\\Finished Files\\" + newFileName + "\\" + newFileName + ".wav")
            audio = AudioSegment.from_wav(folder + "\\Finished Files\\" + newFileName + "\\" + newFileName + ".wav")
            audio.export(folder + "\\Finished Files\\" + newFileName + "\\" + newFileName + ".mp3", format="mp3")
        else:
            os.rename(folder + "\\Finished Files\\" + newFileName + "\\" + fileName, folder + "\\Finished Files\\" + newFileName + "\\" + newFileName + ".mp3")


print (Style.BRIGHT)
folder = intro()
fileRenamer(folder)