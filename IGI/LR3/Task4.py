import time

"""
in the line «So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid,
 whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, 
 when suddenly a White Rabbit with pink eyes ran close by her.» 
You need to: 
a) determine the number of words whose length is less than 5;
b) find the shortest word ending with the letter 'd';
c) output all the words in descending order of their length
"""

def decorator(func):
    
    def wrapper(*str):
        start = time.time()
        result = func(*str)
        end = time.time()
        print("Время выполнения", end - start,"секунд")
        return result
    return wrapper

@decorator
def Task4():
    text = ("So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy "
            "and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and"
            " picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.")

    text_list = text.replace(",","").split()
    length = [x for x in text_list if len(x) < 5]
    print(f"А)Количество слов длинна которых < 5 {len(length)}")

    d_length = [x for x in text_list if x.endswith('d')]
    short = min(d_length,key=len)
    print(f"Б)Самое короткое слово оканчивающиеся на 'd': {short}")
    #print(str.lower.__doc__)
    sorted_words = sorted(text_list, key=lambda x: (-len(x), x.lower()))

    print("в)Слова в порядке убывания их длин  ",", ".join(sorted_words))

    for _ in range(1_000_000):
        pass