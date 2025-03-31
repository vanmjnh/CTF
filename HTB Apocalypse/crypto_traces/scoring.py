import math

FREQ = {'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610,  
        'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513,  
        'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134,  
        'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182}

def bhattacharyya_distance(dist1: dict, dist2: dict) -> float:
    bc_coeff = 0

    for letter in FREQ.keys():
        value1 = dist1.get(letter, 0)  # Tránh KeyError
        value2 = dist2.get(letter, 0)
        bc_coeff += math.sqrt(value1 * value2)

    # Tránh log(0) bằng cách đảm bảo bc_coeff > 0
    return -math.log(bc_coeff) if bc_coeff > 0 else float('inf')

def score_string(word: bytes) -> float:  
    curr_freq = {letter: 0 for letter in FREQ.keys()}  

    # Tính tần suất ký tự trong từ hiện tại  
    num_letters = 0  
    for i in word:  
        char = chr(i).lower()
        if char in curr_freq:  # Tránh KeyError
            curr_freq[char] += 1  
            num_letters += 1  

    if num_letters == 0:  
        return 0  

    # Chuẩn hóa tần suất  
    curr_freq = {letter: val / num_letters for letter, val in curr_freq.items()}  

    # Tính khoảng cách Bhattacharyya  
    distance = bhattacharyya_distance(FREQ, curr_freq)  

    # Tránh chia cho 0
    return 1 / distance if distance > 0 else 0


