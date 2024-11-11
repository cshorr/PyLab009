# Creating a One-Time Pad Book Cipher

---

**Objective**: Guide students to create a one-time pad book cipher that uses multiple textbooks to build a larger book and generates a cipher based on page number, line number, and character position. The lab will involve structuring and building functions for data cleaning, processing, and encryption/decryption.

---

## Part 1: Understanding the Problem and Planning

1. **Problem Overview**: This is a one-time pad book cipher. Each character in a plaintext message is mapped to a unique page, line, and position in a large text code-book.

2. **High-Level Flow**: This is our generic process:
    * Text cleaning and processing
    * Book combining and indexing by page, line, and character
    * Building the codebook for character mapping
    * Encrypting and decrypting messages

3. **Generalization Discussion**: We will use functions to generalized or text processing into functions re-usable for numerous text processing purposes. We will also use functions to build the data-structures necessary for us to map plaintext to ciphertext and vis-versa. Finally, there are several global variables we will need to properly process Gutenberg Press books into our desired structures. At the very top of your Python code, add the following necessary global variables.
```python
HOW_MANY_BOOK = 3
LINE = 128
PAGE = 64
pages = {}
page_number=0
line_window = {}
line_number = 0
char_window = []
```

---

## Part 2: Preparing and Cleaning Text

1. **Cleaning Text**:
    * Create a `clean_line(line)` function to remove multiple whitespaces, handle dashes, and add space at the end of lines for spacing consistency.
```python
def clean_line(line):
    return line.strip().replace( '-', '' ) + ' '  # Adding a space instead of a newline.
```

2. **Reading a Book File**:
    * Define a `read_book(file_path)` function.
    * Load a text file and read lines one by one.
    * For now assume process_char, add_line, and add_page exist as we will add them later.
        * process_char is a windowing function that will process characters until we have a full line.
        * add_line is technically part of process_char, but gets generalized since its code would be duplicated in read_book to handle the last incomplete line of characters.
        * add_page is technically part of future function process_page, but gets generalized since its code would be duplicated in read_book to handle the last incomplete page of lines.
```python
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
```

---

## Part 3: Building Page and Line Buffers

1. **Buffering Lines / Line Windowing**:
    * Introduce `process_char(char)` to accumulate characters into lines. `process_char()` is a generalized function to store lines when they reach a specified length (`LINE` constant).
    * `add_line()` is technically part of process_char, but gets generalized since its code would be duplicated in read_book to handle the last incomplete line of characters.
        * `add_line()` also resets the character window buffer.
```python
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
```
   
2. **Buffering Pages / Page Windowing**:
    * Define `process_page(line, line_number)` to accumulate lines into pages. `process_page()` is used to store lines into a page dictionary when a page reaches a set length (`PAGE` constant).
    * `add_page()` is technically part of process_page, but gets generalized since its code would be duplicated in read_book to handle the last incomplete page of lines.
        * `add_page` also resets the page buffer.
```python
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
```

3. **Scaffolding Tip**: As you're writing these functions, make sure to test them and write or copy over small, manageable chunks of code that build up to a complete page and line storage solution. Add print statements to debug. These scaffolding techniques will make your code more manageable.

---

## Part 4: Combining Multiple Books

1. **Reading Multiple Books**:
    * Implement `process_books(*paths)` to combine multiple book files and pass each to `read_book`.
```python
def process_books(*paths):
    for path in paths:
        read_book( path )
```

2. **Generalization Discussion**: What would be some pros and cons of different ways to combine books for greater randomness in your one-time-pad?

---

## Part 5: Building the Codebook

1. **Generating the Codebook**:
    * Implement `generate_code_book()` to create a dictionary where each character maps to a list of page-line-position references.
    * **Scaffolding Tip**: First try building the dictionary without using setdefault and enumerating characters.
    * Note the nested for loops are due to our need to find the page, line, and position for each character in our formatted set of books.
```python
def generate_code_book():
    global pages
    code_book = {}
    for page, lines in pages.items():
        for num, line in lines.items():
            for pos, char in enumerate(line):
                code_book.setdefault(char, []).append(f'{page}-{num}-{pos}')
    return code_book
```

2. **Saving and Loading the Codebook**:
    * Add `import json` at the top of your code file to access the Python json module for loading and dumping Python objects.
    * Define `save(file_path, code_book)` and `load(file_path, *key_books)` for saving and loading the codebook as JSON files.
    * Notice how load will load a codebook file if it already exists (i.e. via json.load), otherwise it creates the codebook from scratch and stores it (i.e. json.dump).
```python
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
```
---

## Part 6: Encryption and Decryption

1. **Encrypting a Message**:
    * Add `import random` to the top of your file to import the random module for randomly selecting a page-line-position ciphertext out of our codebook.
    * Define `encrypt(code_book, message)` to select random mappings for each character.
    * You may want to add handling characters without mappings by throwing an error or skipping, but that is not done here.
```python
def encrypt(code_book, message):
    cipher_text = []
    for char in message:
        index = random.randint(0, len(code_book[char]) - 1)
        cipher_text.append(code_book[char].pop(index))
    return '-'.join(cipher_text)
```

2. **Decrypting a Message**:
    * Define `decrypt(rev_code_book, ciphertext)` to reverse lookup from page-line-position to plaintext characters.
    * Note, for this phase we use the `pages` global structure that we generated in Parts 1 - 4. This is the perfect structure for reversing our encryption, so we saved it earlier and reload it for decryption.
    * Pay attention to how we convert ciphertext to plaintext by using regex to split on the page-line-position delimited ciphertext.
```python
def decrypt(rev_code_book, ciphertext):
    plaintext = []
    for cc in re.findall(r'\d+-\d+-\d+', ciphertext):
        page, line, char = cc.split('-')
        plaintext.append(
            rev_code_book[page][line][int(char)])
    return ''.join(plaintext)
```

---

## Part 7: Main Menu and Putting It All Together

1. **Creating a User Interface**:
    * Implement `main_menu()` and `main()` to present choices for encryption, decryption, and quitting.
    * **Incremental Development Tip**: Test each menu option independently before integrating them.
```python
def main_menu():
    print("""1). Encrypt
2). Decrypt
3). Quit
""");
    return int(input("Make a selection [1,2,3]: "))


def main():
    key_books = ('books/War_and_Peace.txt', 'books/Moby_Dick.txt', 'books/Dracula.txt')
    code_book_path = 'code_books/dmdwp.txt'
    rev_code_book_path = 'code_books/dmdwp_r.txt'
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
```

---

## Part 8: Extending the Code (Optional for Advanced Students)

1. **Enhancing Randomness**:
    * Try rotating codebooks or interweaving pages from different books.
   
2. **Adding Object-Oriented Design**:
    * Explore converting the program to use classes where each book, page, and line is an object containing our global instance variables.

## Part 9: Turn-In

1. You know the drill by now. Create a GitHub repo.
2. Check in your working code
3. Submit your link to Canvas