import re 
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import os, sys
import utils
from pathlib import Path
from os import path




def pdf_to_string(input_path, output_path):
    if len(input_path) == 0 or len(output_path) == 0:
        raise ValueError("Error! The filepath is EMPTY!!")
    
    output_string = StringIO()
    with open(input_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        text = output_string.getvalue()
    with open(output_path, "w",encoding='utf-8') as f:
        f.write(text)
        

def setup(base_dir, output_base_dir):
    please_quit = 0    
    mylist = []
    for root, dirs, files in os.walk(base_dir):  # os.walk allows us to walk through all files in the pdf directory
        temp_root = root.replace(base_dir, output_base_dir)    #base_dir contains all pdfs, output_base_dir will be the converted text dataset
        if not os.path.exists(temp_root):       #if root directory of converted files does not exist, create one mkdir()
            os.mkdir(temp_root)
        for file in files:                       # search for file names and ignore any 
            if file.lower().find(".pdf") == -1:
                continue
            input_temp = os.path.join(root, file)
            output_temp = input_temp.replace(base_dir, output_base_dir)
            output_temp = output_temp.replace(".pdf", ".txt")
            if input_temp.find("Non-English - LT") == -1:
                # If the text file already exists, don't convert it again!
                if os.path.exists(output_temp):
                    continue
                print("Converting {}, ({})".format(file, len(mylist)))
                # ----
                please_quit += 1     # quit converting files after 30 files
                pdf_to_string(input_temp, output_temp)
                mylist.append([input_temp, output_temp])
                if please_quit > 30: 
                    return mylist        



def read_text_file(file_path):
    with open(file_path, 'r', encoding = 'utf-8') as f:
        print(f.read())




def readlist(filepath):
   with open(filepath) as f:
       data = f.readlines()
       data = [re.sub('[\n+]','',i) for i in data]
   return data    

# list_of_strings = readlist(r'C:\Users\15312\OneDrive - University of Nebraska at Omaha\Ayman_desktop\vs codes\highlighted pdfsss\Graphene PDFs\SI_Units.txt')
# print(list_of_strings)




def search_for_matches_in_file(file_name):
    """Get line from the file along with line numbers, which contains any string from the list"""
    sent_number = 0
    list_of_results = []
    line_number = []
    list_of_strings = readlist(r'C:\Users\15312\OneDrive - University of Nebraska at Omaha\Ayman_desktop\vs codes\highlighted pdfsss\Graphene PDFs\SI_Units.txt')
    # Open the file in read only mode
    with open(file_name, 'r',encoding='UTF-8') as read_obj:
        file  = read_obj.read()
        sent_list = re.split('\.\s',file)   #splits sentence after each period
        sent_list = [re.sub('[\n+]',' ',i) for i in sent_list]    #removing unnecesaary tabs in texts
        for sent in sent_list:
            sent_number += 1
            # sent = [re.sub('\s+','',sent)]
            # For each line, check if line contains any string from the list of strings
            for string_to_search in list_of_strings:
                if string_to_search in sent:
                    # If any string is found in line, then append that line along with line number in list
                    list_of_results.append((string_to_search, sent_number, sent.rstrip()))
    # Return list of tuples containing matched string, line numbers and lines where string is found
    return list_of_results


# def save_output(folder):
#     saving_dir = os.chdir(r'C:\Users\15312\OneDrive - University of Nebraska at Omaha\Ayman_desktop\vs codes\highlighted pdfsss\Graphene PDFs\results')
    
#     file = open('output.txt','w',encoding='utf-8')
#     file.write('Total Matched sentences : '+str(len(matched_lines))+'\n\n')
#     for elem in matched_lines:
#             file.write('\n'+ '-> Word = '+ elem[0] +'\n'+ '-> Sentence Number = '+ str(elem[1])+'\n'+ '-> Sentence = '+ elem[2]+'\n\n'+'-'*60+'\n')


def main():
    
    while True:
        action = input("\n\nActions :\n\n1) Convert PDF data to text  2) Search for SI units  3)Save progress: ") # asking the user for an action on the system
        if action == '3':
            print('\n\n-------------------------------ALL FILES SAVED-----------------------------------\n\n')
            break
        
        if action == '1':
            base_dir = input('\nEnter pdf dataset (Expecting a folder name): ')
            output_base_dir = input('\nWhere do you want to keep your converted dataset (Expecting a folder name): ')
            print('\n----------Starting conversion...this may take a while---------------\n\n')
            setup(base_dir,output_base_dir)
            print('\n--------------Successfully converted all PDF to text files!!----------------\n')
        
        
        if action == '2':
            path = r"C:\Users\15312\OneDrive - University of Nebraska at Omaha\Ayman_desktop\vs codes\highlighted pdfsss\Graphene PDFs\text_dataset"
            os.chdir(path)
            # iterate through all file
            for file in os.listdir():
                # Check whether file is in text format or not
                if file.endswith(".txt"):
                    file = input('\nEnter filename: ')
                    file_path = f"{path}\{file}"
                    # matched_lines = search_for_matches_in_file(file_path)
                    saving_dir = os.chdir(r'C:\Users\15312\OneDrive - University of Nebraska at Omaha\Ayman_desktop\vs codes\highlighted pdfsss\Graphene PDFs\results')
                    matched_lines = search_for_matches_in_file(file_path)
                    txt = open(f'output of {file}','w',encoding='utf-8')
                    txt.write('Total Matched sentences : '+str(len(matched_lines))+'\n\n')
                    for elem in matched_lines:
                        txt.write('\n'+ '-> Word = '+ elem[0] +'\n'+ '-> Sentence Number = '+ str(elem[1])+'\n'+ '-> Sentence = '+ elem[2]+'\n\n'+'-'*60+'\n')
                    print('\n\n--------------------------------DONE-----------------------------------\n\n')
                    break 
        
                    # read_text_file(file_path)
                    
                
                 
            

                
    
    
    
    
    
    
    
    # search for given strings in the file '.txt'
    # matched_lines = search_for_matches_in_file(r'C:\Users\15312\OneDrive - University of Nebraska at Omaha\Ayman_desktop\vs codes\highlighted pdfsss\Graphene PDFs\text_dataset\Impermeability of graphene.txt')
    
    # file = open('output.txt','w',encoding='utf-8')
    # file.write('Total Matched sentences : '+str(len(matched_lines))+'\n\n')
    # for elem in matched_lines:
    #         file.write('\n'+ '-> Word = '+ elem[0] +'\n'+ '-> Sentence Number = '+ str(elem[1])+'\n'+ '-> Sentence = '+ elem[2]+'\n\n'+'-'*60+'\n')


if __name__ == '__main__': 
    main()        