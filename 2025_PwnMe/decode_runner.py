from pwn import *

encoded_list = {
    "1337 ...\n": "Leet Speak 1337",
    "He can't imagine finding himself in CTF 150 years later...\n": "Baudot Code",
    "A code based on pairs of dots and dashes. Think of a mix of Morse code and numbers... (AZERTYUIO)\n": "Morbit Cipher",
    "It looks like Morse code, but ... \n": "Wabun Code",
    "He can snap his toes, and has already counted to infinity twice ...\n": "Chuck Norris Unary Code",
    "Hendrix would have had it... \n": "Guitar Chords Notation",
    "what is this charabia ???\n": "Latin Gibberish",
    "Born in 1462 in Germany...\n": "Trithemius Cipher",
    "Did you realy see slumdog millionaire ?\n": "Shankar Speech Defect (Q&A)",
    "": "NATO Phonetic Alphabet"
}

def decode_leet(cipher_text):
    # Bảng ánh xạ Leet -> Ký tự thông thường (phân biệt hoa/thường)
    leet_dict = {
        "4": "A", "\\/": "A", "@": "A", "/-\\": "A",
        "8": "B", "|3": "B", "13": "B",
        "(": "C", "<": "C", "[": "C", "©": "C",
        "[)": "D", "|>": "D", "|)": "D",
        "3": "E", "€": "E", "[-": "E",
        "|=": "F", "/=": "F",
        "9": "G", "(_+": "G",
        "#": "H", "/-/": "H", "[-]": "H", "]-[": "H", ")(-": "H", "(-)": "H", "|-|": "H",
        "1": "I", "'": "I", "!": "I", "|": "I",
        "_|": "J", "_/": "J",
        "|<": "K", "|{": "K",
        "|_": "L", "[_": "L", "£": "L", "1_": "L",
        "|V|": "M", "|\\/|": "M", "/\\/\\": "M", "/V\\": "M",
        "|\\|": "N", "/\\/": "N", "[\\]": "N", "/V": "N",
        "[]": "O", "0": "O", "()": "O", "<>": "O",
        "|*": "P", "|o": "P", "|°": "P", "/*": "P",
        "()_": "Q", "0_": "Q", "°|": "Q", "(_,": "Q",
        "|?": "R", "®": "R", "|2": "R",
        "5": "S", "$": "S", "§": "S",
        "7": "T", "†": "T", "¯|¯": "T",
        "(_)": "U", "|_|": "U", "µ": "U",
        "\\/": "V", "|/": "V",
        "\\/\\/": "W", "vv": "W", "\\^/": "W", "\\|/": "W", "\\_|_/": "W",
        "><": "X", "×": "X", ")(": "X",
        "`/": "Y", "¥": "Y", "\\/": "Y",
        "7_'": "Z", ">_": "Z", "≥": "Z",
    }
    
    # Giải mã chuỗi mã hóa (giữ nguyên chữ hoa & thường)
    decoded_text = ''
    for char in cipher_text:
        if char in leet_dict:
            decoded_text += leet_dict[char]  # Chữ hoa
        elif char in leet_dict:
            decoded_text += leet_dict[char]  # Chữ thường
        else:
            decoded_text += char  # Giữ nguyên nếu không phải ký tự Leet

    return decoded_text

def decode_baudot(encoded_binary):
    baudot_letters = {
        "00000": "", "00100": " ", "10111": "Q", "10011": "W", "00001": "E",
        "01010": "R", "10000": "T", "10101": "Y", "00111": "U", "00110": "I",
        "11000": "O", "10110": "P", "00011": "A", "00101": "S", "01001": "D",
        "01101": "F", "11010": "G", "10100": "H", "01011": "J", "01111": "K",
        "10010": "L", "10001": "Z", "11101": "X", "01110": "C", "11110": "V",
        "11001": "B", "01100": "N", "11100": "M", "01000": "\r", "00010": "\n",
        "11011": "<DIGITS>"
    }
    
    baudot_digits = {
        "00000": "", "00100": " ", "10111": "1", "10011": "2", "00001": "3",
        "01010": "4", "10000": "5", "10101": "6", "00111": "7", "00110": "8",
        "11000": "9", "10110": "0", "00011": "-", "00101": "\a", "01001": "$",
        "01101": "!", "11010": "&", "10100": "#", "01011": "'", "01111": "(",
        "10010": ")", "10001": "\"", "11101": "/", "01110": ":", "11110": ";",
        "11001": "?", "01100": ",", "11100": ".", "01000": "\r", "00010": "\n",
        "11011": "<LETTERS>"
    }
    
    mode = "LETTERS"  # Bắt đầu với chế độ chữ cái
    decoded_text = ""
    encoded_binary = encoded_binary.replace(" ", "")
    
    for i in range(0, len(encoded_binary), 5):
        chunk = encoded_binary[i:i+5]
        
        if mode == "LETTERS":
            char = baudot_letters.get(chunk, "?")
            if char == "<DIGITS>":
                mode = "DIGITS"
            else:
                decoded_text += char
        else:
            char = baudot_digits.get(chunk, "?")
            if char == "<LETTERS>":
                mode = "LETTERS"
            else:
                decoded_text += char
    
    return decoded_text

def decode_morbit(ciphertext, keyword="AEIORTUYZ"):

    morse_pairs = ["..", "./", "/-", "//", "-.", "--", "/.", "-/", ".-"]
    
    # Tạo ánh xạ index từ keyword
    sorted_keyword = sorted([(char, i) for i, char in enumerate(keyword)])
    index_mapping = {char: str(i + 1) for i, (char, _) in enumerate(sorted_keyword)}
    index_to_morse = {str(i + 1): morse_pairs[idx] for idx, (char, i) in enumerate(sorted_keyword)}
    
    # Giải mã dãy số thành mã Morse
    morse_code = ''.join(index_to_morse[digit] for digit in ciphertext)
    
    # Tách Morse code thành từng ký tự
    morse_words = morse_code.split('//')
    morse_dict = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
        '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8',
        '----.': '9'
    }
    
    plaintext = ''
    for word in morse_words:
        morse_chars = word.split('/')
        plaintext_word = ''.join(morse_dict.get(char, char) for char in morse_chars)
        plaintext += plaintext_word + ' '
    
    return plaintext

def decode_wabun(morse_code):

    wabun_dict = {
    ".-": "i", "-.-": "wa", ".-..-": "wi", "-.-.-": "sa",
    ".-.-": "ro", ".-..": "ka", "..--": "no", "-.-..": "ki",
    "-...": "ha", "--": "yo", ".-...": "o", "-..--": "yu",
    "-.-.": "ni", "-.": "ta", "...-": "ku", "-...-": "me",
    "-..": "ho", "---": "re", ".--": "ya", "..-.-": "mi",
    ".": "he", "---.": "so", "-..-": "ma", "--.-.": "shi",
    "..-..": "to", ".--.": "tsu", "-.--": "ke", ".--..": "we",
    "..-.": "chi", "--.-": "ne", "--..": "fu", "--..-": "hi",
    "--.": "ri", ".-.": "na", "----": "ko", "-..-.": "mo",
    "....": "nu", "...": "ra", "-.---": "e", ".---.": "se",
    "-.--.": "ru", "-": "mu", ".-.--": "te", "---.-": "su",
    ".---": "wo", "..-": "u", "--.--": "a", ".-.-.": "n"
    }
    words = morse_code.split()
    decoded_text = "".join(wabun_dict.get(code, code) for code in words)
    return decoded_text

def decode_chuck_norris_unary(cipher_text):
    # Chia văn bản thành các khối mã unary
    blocks = cipher_text.split()
    binary_string = ''
    
    for i in range(0, len(blocks), 2):
        bit_value = '0' if blocks[i] == '00' else '1'
        binary_string += bit_value * len(blocks[i + 1])
    
    # Chia chuỗi nhị phân thành các đoạn 7 bit
    characters = [binary_string[j:j+7] for j in range(0, len(binary_string), 7)]
    
    # Chuyển đổi từng đoạn nhị phân thành ký tự ASCII
    decoded_text = ''.join(chr(int(char, 2)) for char in characters if char)
    
    return decoded_text

def decode_guitar_chords_notation(progression):
    """
    Giải mã một chuỗi hợp âm guitar từ ký hiệu thành tên hợp âm.
    
    Thông số:
    progression (str): Chuỗi chứa các ký hiệu hợp âm, cách nhau bởi dấu cách.
    
    Trả về:
    str: Chuỗi hợp âm được định danh, cách nhau bởi dấu cách.
    """
    chord_positions = {
        "x24442": "B",
        "x02220": "A",
        "133211": "F",
        "022100": "E",
        "xx0232": "D",
        "320003": "G",
        "x32010": "C",
        "x35553": "C#",
        "355433": "G#",
        "577655": "A",
        "799877": "B",
        "x57775": "D",
        "x79997": "E",
    }
    
    chord_notations = progression.split()
    return ''.join([chord_positions.get(notation, "UNKNOWN") for notation in chord_notations])

def decode_latin_gibberish(text):
    """
    Giải mã văn bản được mã hóa bằng mật mã Latin Gibberish.
    
    Thông số:
    text (str): Chuỗi văn bản Latin Gibberish cần giải mã.
    
    Trả về:
    str: Văn bản đã được giải mã.
    """
    import re
    
    # Danh sách hậu tố Latin phổ biến trong mật mã Latin Gibberish
    latin_suffixes = ["us", "um", "it", "ae", "is", "os", "es"]
    
    words = text.split()
    decoded_words = []
    
    for word in words:
        # Loại bỏ hậu tố Latin nếu có
        for suffix in latin_suffixes:
            if word.endswith(suffix):
                word = word[: -len(suffix)]
                break
        
        # Đảo ngược từ để lấy lại từ gốc
        decoded_words.append(word[::-1])
    
    return ' '.join(decoded_words)

def decode_trithemius_cipher(text, key=3):
    """
    Giải mã văn bản được mã hóa bằng Trithemius Cipher với một khóa dịch chuyển.
    
    Thông số:
    text (str): Chuỗi văn bản đã được mã hóa.
    key (int): Giá trị khóa dịch chuyển ban đầu.
    
    Trả về:
    str: Văn bản gốc sau khi giải mã.
    """
    decoded_text = ""
    
    for i, char in enumerate(text):
        if char.isalpha():
            shift = (key + i) % 26  # Dịch chuyển thay đổi theo vị trí và khóa
            if char.islower():
                decoded_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                decoded_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            decoded_char = char  # Giữ nguyên ký tự không phải chữ cái
        
        decoded_text += decoded_char
    
    return decoded_text

def decode_shankar_speech_defect(encoded_text):
    """
    Giải mã cipher sử dụng bảng mã hóa ABCDEFGHIJKLMNOPQRSTUVWXYZ -> XWYAZBCDQEFGHIKLMNOPJRSTUV
    
    Thông số:
    encoded_text (str): Văn bản đã mã hóa.
    
    Trả về:
    str: Văn bản gốc đã giải mã.
    """
    # Bảng mã hóa ngược
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cipher_key = "XWYAZBCDQEFGHIKLMNOPJRSTUV"

    # Tạo bảng mã hóa ngược
    reverse_cipher_map = {cipher_key[i]: alphabet[i] for i in range(len(alphabet))}

    # Giải mã văn bản
    decoded_text = ""
    for char in encoded_text:
        if char.upper() in reverse_cipher_map:
            # Kiểm tra nếu chữ cái là viết hoa
            if char.isupper():
                decoded_text += reverse_cipher_map[char.upper()]
            else:
                decoded_text += reverse_cipher_map[char.upper()].lower()
        else:
            decoded_text += char

    return decoded_text

def decode_nato_cipher(encoded_text):
    """
    Giải mã văn bản được mã hóa bằng bảng chữ cái ICAO (NATO Phonetic Alphabet).
    
    Thông số:
    encoded_text (str): Chuỗi văn bản ICAO cần giải mã.
    
    Trả về:
    str: Văn bản gốc sau khi giải mã.
    """
    return "".join(word[0] for word in encoded_text.split())

def decode_runner():
    # r = remote("decoderunner-6cb23dc19c88b77c.deploy.phreaks.fr", 443, ssl=True)
    r = process("python", "build/src/DECODE_RUNNER.py")
    r.recvuntil(b'Good luck!\n\n\n\n')

    for i in range(100):
        recieve = r.recv().decode().strip().replace("hint: ", "").split("cipher: ")
        hint, ct = recieve[0], recieve[1]
        print(f"[{i}] {hint: }\n{ct: }")

        if encoded_list[hint] == "Leet Speak 1337":
            pt = decode_leet(ct).lower()
            print(f"{pt: }")
            r.sendline(pt.encode())

        elif encoded_list[hint] == "Baudot Code":
            pt = decode_baudot(ct).lower()
            print(f"{pt: }")
            r.sendline(pt.encode())

        elif encoded_list[hint] == "Morbit Cipher":
            pt = decode_morbit(ct).lower()
            print(f"{pt: }")
            r.sendline(pt.encode())

        elif encoded_list[hint] == "Wabun Code":
            pt = decode_wabun(ct).lower()
            print(f"{pt: }")
            r.sendline(pt.encode())

        elif encoded_list[hint] == "Chuck Norris Unary Code":
            pt = decode_chuck_norris_unary(ct).lower()
            print(f"{pt: }")
            r.sendline(pt.encode())

        elif encoded_list[hint] == "Guitar Chords Notation":
            pt = decode_guitar_chords_notation(ct).lower()
            print(f"{pt: }")
            r.sendline(pt.encode())

        elif encoded_list[hint] == "Latin Gibberish":
            pt = decode_latin_gibberish(ct).lower()
            print(f"{pt: }")
            r.sendline(pt.encode())

        elif encoded_list[hint] == "Trithemius Cipher":
            pt = decode_trithemius_cipher(ct).lower()
            print(f"{pt: }")
            r.sendline(pt.encode())

        elif encoded_list[hint] == "Shankar Speech Defect (Q&A)":
            pt = decode_shankar_speech_defect(ct).lower()
            print(f"{pt: }")
            r.sendline(pt.encode())

        elif encoded_list[hint] == "NATO Phonetic Alphabet":
            pt = decode_nato_cipher(ct).lower()
            print(f"{pt: }")
            r.sendline(pt.encode())

        else:
            print("This cipher is not in list!")

    print(r.recvall())

    r.close()

decode_runner()
