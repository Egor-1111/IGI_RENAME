import re
import zipfile
import Input_data
"""
Output the source text by replacing spaces with a character entered from the keyboard
Determine whether a given GUID string is with or without parentheses. A GUID is a string consisting of 8, 4, 4, 4, 12 hexadecimal digits separated by a dash. An example of a correct expression: e02fd0e4-00fd-090A-ca30- 0d00a0038ba0. Example of an incorrect expression: e02fd0e400fd090Aca300d00a0038ba0.
determine the number of uppercase lowercase letters;
find the first word containing the letter 'z' and its number;
output a string by excluding words starting with 'a' from it
"""
class TextAnalyzer:

    def __init__(self, text):
        self.text = text

    def count_sentences(self):
        sentences = re.split(r'[.!?]+', self.text)
        num_sentences = 1
        if len(sentences) != 1:
            num_sentences = len(sentences) - 1
        return num_sentences

    def count_narrative_sentences(self):
        narrative_sentences = re.findall(r'[А-ЯA-Z][^.!?]*[.]', self.text)
        num_narrative_sentences = len(narrative_sentences)
        return num_narrative_sentences

    def count_interrogative_sentences(self):
        interrogative_sentences = re.findall(r'[А-ЯA-Z][^.!?]*[?]', self.text)
        num_interrogative_sentences = len(interrogative_sentences)
        return num_interrogative_sentences

    def count_imperative_sentences(self):
        imperative_sentences = re.findall(r'[А-ЯA-Z][^.!?]*!', self.text)
        num_imperative_sentences = len(imperative_sentences)
        return num_imperative_sentences

    def calculate_average_sentence_length(self):
        sentences = re.split(r'[.!?]+', self.text)
        num_sentences = len(sentences)
        total_sentences_length = 0
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence)
            total_sentences_length += sum(len(word) for word in words)
        average_sentence_length = total_sentences_length / num_sentences
        return average_sentence_length

    def calculate_average_word_lenght(self):
        words = re.findall(r'\b\w+\b', self.text)
        total_word_length = sum(len(word) for word in words)
        average_word_length = total_word_length / len(words)
        return average_word_length

    def count_smileys(self):
        smileys = re.findall(r'[;:]-*[()\[\]]+', self.text)
        num_smileys = len(smileys)
        return num_smileys

    def replace_spaces(self,input):
        short_words = re.sub(r' ',input, self.text)
        return short_words

    def is_valid_guid(self):
        pattern = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
        highlighted_text = re.findall(pattern, self.text)
        return highlighted_text

    def analyze_text_with_regex(self):
        uppercase = re.findall(r'[A-ZА-Я]', self.text)
        lowercase = re.findall(r'[a-zа-я]', self.text)
        return uppercase,lowercase

    def find_first_z_word_and_position(self):

        words_with_pos = [(m.group(), m.start()) for m in re.finditer(r'\b\w+\b', self.text)]

        for i, (word, pos) in enumerate(words_with_pos, 1):
            if re.search(r'z', word, re.IGNORECASE):

                return (word, i)

        return (None, None)

    def remove_words_starting_with_a(self):

        cleaned_text = re.sub(r'\b[aA]\w*\b','',self.text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        return cleaned_text


def write_file(output_file, content):
    with open(output_file, "w") as file:
        file.write(content)


def create_zip_archive(output_file, file_to_archive):
    with zipfile.ZipFile(output_file, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(file_to_archive)
        archive_info = zip_file.getinfo(file_to_archive)
        print("Имя файла в архиве: {}".format(archive_info.filename))
        print("Размер сжатого файла: {} байт".format(archive_info.compress_size))
        print("Размер несжатого файла: {} байт".format(archive_info.file_size))
        print("Метод сжатия: {}".format(archive_info.compress_type))


class DataWorker(TextAnalyzer):
    def __init__(self, input_file, text):

        super().__init__(text)
        self.input_file = input_file
        self.text = self.read_file()

    def read_file(self):
        with open(self.input_file, "r", encoding='utf-8') as file:
            text = file.read()
        return text

    def analyze_text(self):
        num_sentences = self.count_sentences()
        num_narrative_sentences = self.count_narrative_sentences()
        num_interrogative_sentences = self.count_interrogative_sentences()
        num_imperative_sentences = self.count_imperative_sentences()
        average_sentence_length = self.calculate_average_sentence_length()
        average_word_length = self.calculate_average_word_lenght()
        num_smileys = self.count_smileys()
        input = Input_data.input_data("Введите символ для замены пробелу", str)
        replace_text = self.replace_spaces(input)
        highlighted_text = self.is_valid_guid()
        uppercase,lowercase = self.analyze_text_with_regex()
        ferst_z = self.find_first_z_word_and_position()
        repeated_words = self.remove_words_starting_with_a()
        output_content = ""
        output_content += "Количество предложений в тексте: {}\n".format(num_sentences)
        output_content += "Количество повествовательных предложений: {}\n".format(num_narrative_sentences)
        output_content += "Количество вопросительных предложений: {}\n".format(num_interrogative_sentences)
        output_content += "Количество побудительных предложений: {}\n".format(num_imperative_sentences)
        output_content += "Средняя длина предложения в символах: {}\n".format(average_sentence_length)
        output_content += "Средняя длина слова в символах: {}\n".format(average_word_length)
        output_content += "Количество смайликов в тексте: {}\n".format(num_smileys)
        output_content += "Текст без пробелов: {}\n".format(replace_text)
        output_content += "GUID строки: {}\n".format(highlighted_text)
        output_content += "Количество заглавных{} и строчных букв {}\n".format(len(uppercase),len(lowercase))
        output_content += "Первое слово, содержащее букву 'z' и его номер: {}\n".format(ferst_z)
        output_content += "Вывести текст исключая слова начинающиеся на 'a': {}\n".format(repeated_words)
        return output_content


def Task2():
    data_worker = DataWorker("Task2_input.txt", "Task2_output.txt")
    output_content = data_worker.analyze_text()
    write_file("Task2_output.txt", output_content)

    with open("Task2_output.txt", "r") as file:
        file_content = file.read()
        print(file_content)

    create_zip_archive("Task2_result.zip", "Task2_output.txt")