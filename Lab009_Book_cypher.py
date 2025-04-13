# Chris shortt 4/13/2025: this was a hard one, even though it was copy and paste there was a lot of new stuff and even some old stuff i dont quite understand yet. 
import json
import os
import random
import re
from random import randint
import sys


def save(file_path, code_book):

    HOW_MANY_BOOK = 3
LINE = 128
PAGE = 64
pages = {}
page_number=0
line_window = {}
line_number = 0
char_window = []

def clean_line(line):
    return line.strip().replace( '-', '' ) + ' ' # Adding a space instead of a newline

def process_books(*paths):
    for path in paths:
       # print(f'Reading {path}')
        read_book( path )
        #print(f'{len(pages)}, {len(pages[1])} , {pages[len(pages)]}')

def read_book(file_path):
    global char_window
    with open(file_path, 'r', encoding='utf-8-sig') as fp:
        for line in fp:
            line = clean_line(line)
            if line.strip():
                for c in line:
                    process_char(c)

    if len(char_window) > 0:
        add_line()
    if len(line_window) > 0:
        add_page()

def process_char(char):
    global char_window
    char_window.append(char)
    if len(char_window) == LINE:
        add_line()

def add_line():
    global char_window, line_number
    line_number += 1
    process_page( ''.join(char_window), line_number )
    char_window.clear()

def process_page(line, line_num):
    global line_window, pages, page_number
    line_window[line_num] = line
    if len(line_window) == PAGE:
        add_page()

def add_page():
    global line_number, line_window, pages, page_number
    page_number += 1
    pages[page_number] = dict( line_window )
    line_window.clear()
    line_number = 0



# BUILDING THE CODEBOOK !!!!!!!!!!!!!!!
def generate_code_book():
    global pages
    code_book = {}
    for page, lines in pages.items():
        for num, line in lines.items():
            for pos, char in enumerate(line):
                code_book.setdefault(char, []).append(f'{page}-{num}-{pos}')
    return code_book


def save(file_path, book):
    with open(file_path, 'w') as fp:
        # json.dump(book, fp, indent=4)
        json.dump(book, fp)


def load(file_path, *key_books, reverse=False):
    if os.path.exists(file_path):
        with open(file_path, 'r') as fp:
            return json.load(fp)
    else:
        process_books(*key_books)
        if reverse:
            save(file_path, pages)
            return pages
        else:
            code_book = generate_code_book()
            save(file_path, code_book)
            return code_book

def encrypt(code_book, message):
    cipher_text = []
    for char in message:
        index = random.randint(0, len(code_book[char]) - 1)
        cipher_text.append(code_book[char].pop(index))
    return '-'.join(cipher_text)


def encrypt(code_book, message):
    cipher_text = []
    for char in message:
        index = random.randint(0, len(code_book[char]) - 1)
        cipher_text.append(code_book[char].pop(index))
    return '-'.join(cipher_text)

def decrypt(rev_code_book, ciphertext):
    plaintext = []
    for cc in re.findall(r'\d+-\d+-\d+', ciphertext):
        page, line, char = cc.split('-')
        plaintext.append(
            rev_code_book[page][line][int(char)])
    return ''.join(plaintext)

#             load( './code_books/book1_r.json', './books/GreatGatsby.txt', './books/Tess.txt', reverse=True), ciphertext))

def main_menu():
    print("""1). Encrypt
2). Decrypt
3). Quit
""");
    return int(input("Make a selection [1,2,3]: "))


def main():
    key_books = ('books/Gullivers_Travels.txt', 'books/shakespeare.txt', 'books/tess.txt', 'books/GreatGatsby.txt')
    code_book_path = 'code_books/book2.json'
    rev_code_book_path = 'code_books/book2_r.json'
    while True:
        try:
            choice = main_menu()
            match(choice):
                case 1:
                    code_book = load( code_book_path, *key_books )
                    message = input("Please enter your secret message: ")
                    print(encrypt(code_book, message))
                    continue;
                case 2:
                    rev_code_book = load( rev_code_book_path, *key_books, reverse=True)
                    message = input("Please enter your cipher text: ")
                    print( decrypt( rev_code_book, message ) )
                    continue;
                case 3:
                    sys.exit(0)
        except ValueError as ve:
            print("Improper selection.")


if __name__ == '__main__':
    main()


# process_books( './books/GreatGatsby.txt','./books/Tess.txt' )
# cb = generate_code_book()
# save('./code_books/book1.json', cb)
#cb = load('./code_books/book1_r.json', './books/GreatGatsby.txt','./books/Tess.txt' , reverse = True)
#print(cb)
# message = input(" type your secret message: ")
# print(
#     encrypt(
#         load('./code_books/book1.json', './books/GreatGatsby.txt','./books/Tess.txt' , ) , message))
# ciphertext = '88-46-106-92-33-45-100-50-80-64-19-2-17-50-75-50-1-40-33-45-110-54-57-17-89-16-84-44-57-80-42-38-0-139-58-91-34-51-83-63-29-25-103-35-74-125-59-22-94-1-91-85-11-120-11-45-13-67-39-109-80-49-104-110-62-16-91-47-74-56-45-119-52-33-103-58-55-82-136-39-14-60-8-26-101-8-117-15-59-9-52-24-127-24-57-7-81-32-40-16-11-2-34-17-106-133-16-70-85-61-118-139-10-99-7-19-87'
# print(
# decrypt(
