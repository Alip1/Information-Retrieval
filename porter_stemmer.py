class PorterStemmer:
    def __init__(self):
        self.word = None
        self.vowel_seq = None
        self.r1 = None
        self.r2 = None

    def word_stemming(self, word):
        # # Here we check if the word is already is lower case or not. if it is we don't cast it into lower case
        # otherwise we do then we reset the regions and do pre-processing of the words.then we do some pre-processing
        # of word that needs to be stemmed in order to remove the irregularities and if the length of the word is
        # less than or equal to 2 we return from here as no stemming can be performed. then we perform each step of
        # Porter Algorithm step by step and then return the word
        if not word.islower():
            self.word = word.lower()
        else:
            self.word = word
        self.regions_to_be_reset()
        self.pre_processing_of_words()

        if len(self.word) <= 2:
            return self.word

        self.porter_algo_step_1a()
        self.porter_algo_step_1b()
        self.porter_algo_step_1c()
        self.porter_algo_step_2()
        self.porter_algo_step_3()
        self.porter_algo_step_4()
        self.porter_algo_step_5a()
        self.porter_algo_step_5b()

        return self.word

    def regions_to_be_reset(self):
        # Resetting the region everytime an object of this Porter class would be created
        self.vowel_seq = 'aeiou'
        self.r1 = ''
        self.r2 = ''

    def pre_processing_of_words(self):
        # Preprocessing the words to remove any irregularities
        if self.word.startswith('\''):
            self.word = self.word[1:]

        if self.word.endswith('\'s'):
            self.word = self.word[:-2]

        if self.word.endswith('sses'):
            self.word = self.word[:-2]
        elif self.word.endswith('ies'):
            self.word = self.word[:-2] + 'i'
        elif self.word.endswith('ss'):
            pass
        elif self.word.endswith('s'):
            self.word = self.word[:-1]

        # Update the regions
        self.updating_regions_of_word()

    def updating_regions_of_word(self):
        # updating the region of word
        self.r1 = self.word
        if 'y' in self.word:
            y_index = self.word.index('y')
            if y_index > 0:
                self.r1 = self.word[y_index + 1:]

        if 'y' in self.r1:
            y_index = self.r1.index('y')
            self.r2 = self.r1[y_index + 1:]

    def _ends_with(self, suffix):
        # checking whether the word ends with the suffix or not
        return self.word.endswith(suffix)

    def word_ends_with_vowel_consonant(self):
        # Checking if the word is ending with vowel or consonant
        if len(self.word) < 2:
            return False

        return self.word[-2] not in self.vowel_seq and self.word[-1] in self.vowel_seq

    def suffix_to_be_replaced(self, suffix, replacement, region):
        # replacing the suffix with the replaced word
        if self.word.endswith(suffix):
            self.word = self.word[:len(self.word) - len(suffix)] + replacement

            if len(self.word) >= len(region):
                self.updating_regions_of_word()

    def stemmability_measure(self, region):
        # returning the count that how much time VC appeared together
        converted = self.convert_to_vowel_consonant_format(region)
        count = 0

        for i in range(len(converted) - 1):
            if converted[i:i + 2] == "VC":
                count += 1

        return count

    def convert_to_vowel_consonant_format(self, word):
        # Converting the word into vowel consonant format, in order to calculate the stemmability measure
        vowels = "AEIOUaeiou"
        converted = ""

        for char in word:
            if char.isalpha():
                if char in vowels:
                    converted += "V"
                else:
                    converted += "C"

        return converted

    def porter_algo_step_1a(self):
        # in this first step we check whether the word ends with sses. if yes then we remove the last sses and
        # replace it with ss. if the word ends with ies we replace it with i if the word ends with ss with pass it.
        # and if only contains s we remove it
        if self.check_word_ends_with_suffix('sses'):
            self.word = self.word[:-2]
        elif self.check_word_ends_with_suffix('ies'):
            self.word = self.word[:-3] + 'i'
        elif self.check_word_ends_with_suffix('ss'):
            pass
        elif self.check_word_ends_with_suffix('s'):
            self.word = self.word[:-1]

        # Update the regions
        self.updating_regions_of_word()

    def porter_algo_step_1b(self):
        # this method handles that if a word ends with "EED" and has a measure greater than 0 (i.e., a count of
        # vowel-consonant sequences), it is modified to end with "EE." If a word ends with "ED" and satisfies the
        # condition of having a vowel before the "ED," the suffix "ED" is removed. If a word ends with "ING" and
        # satisfies the condition of having a vowel before the "ING," the suffix "ING" is removed.
        # "I read the porter.txt file and found your note."
        if self.check_word_ends_with_suffix('eed'):
            if self.stemmability_measure(self.r1[:-3]) > 0:
                self.word = self.word[:-1]
        elif self.check_word_ends_with_suffix('ed'):
            if self.word.endswith('ed'):
                if any(c in self.r1[:-2] for c in self.vowel_seq):
                    self.word = self.word[:-2]
                    self.updating_regions_of_word()
                    if self.check_word_ends_with_suffix('at'):
                        self.word += 'e'
                    elif self.check_word_ends_with_suffix('bl'):
                        self.word += 'e'
                    elif self.check_word_ends_with_suffix('iz'):
                        self.word += 'e'
                    elif self.word_ends_with_vowel_consonant() and not self.check_word_ends_with_suffix(
                            'l') and not self.check_word_ends_with_suffix('s') and not self.check_word_ends_with_suffix(
                        'z'):
                        if self.stemmability_measure(self.r1) > 0:
                            self.word += 'e'
        elif self.check_word_ends_with_suffix('ing'):
            if self.word.endswith('ing'):
                if any(c in self.r1 for c in self.vowel_seq):
                    self.word = self.word[:-3]
                    self.updating_regions_of_word()
                    if self.check_word_ends_with_suffix('at'):
                        self.word += 'e'
                    elif self.check_word_ends_with_suffix('bl'):
                        self.word += 'e'
                    elif self.check_word_ends_with_suffix('iz'):
                        self.word += 'e'
                    elif self.word_ends_with_vowel_consonant() and not self.check_word_ends_with_suffix(
                            'l') and not self.check_word_ends_with_suffix('s') and not self.check_word_ends_with_suffix(
                        'z'):
                        if self.stemmability_measure(self.r1) > 0:
                            self.word += 'e'

        # Update the regions
        self.updating_regions_of_word()

    def porter_algo_step_1c(self):
        # this method or step focuses on addressing the conversion of words from their "Y" form to their stem form
        # when specific conditions are met. It replaces the "Y" with "I" to obtain the stem of the word. Example:
        # "happy" becomes "happi", "sky" remains "sky".
        if self.check_word_ends_with_suffix('y') and any(c in self.r1 for c in self.vowel_seq):
            self.word = self.word[:-1] + 'i'

        # Update the regions
        self.updating_regions_of_word()

    def porter_algo_step_2(self):
        # this method or step handles the specific suffixes and transforming them to their respective forms. The
        # transformations are based on the penultimate letter of the word being tested. Here I have taken a list a
        # suffixes and then measure its stemmability and then replace it with the corresponding one
        word_suffixes = [
            ('ational', 'ate', self.r1),
            ('tional', 'tion', self.r1),
            ('enci', 'ence', self.r1),
            ('anci', 'ance', self.r1),
            ('izer', 'ize', self.r1),
            ('abli', 'able', self.r1),
            ('alli', 'al', self.r1),
            ('entli', 'ent', self.r1),
            ('eli', 'e', self.r1),
            ('ousli', 'ous', self.r1),
            ('ization', 'ize', self.r2),
            ('ation', 'ate', self.r2),
            ('ator', 'ate', self.r2),
            ('alism', 'al', self.r2),
            ('iveness', 'ive', self.r2),
            ('fulness', 'ful', self.r2),
            ('ousness', 'ous', self.r2),
            ('aliti', 'al', self.r2),
            ('iviti', 'ive', self.r2),
            ('biliti', 'ble', self.r2)
        ]

        for suffix in word_suffixes:
            if self.check_word_ends_with_suffix(suffix[0]) & self.stemmability_measure(self.r1[:-len(suffix[0])]) > 0:
                self.suffix_to_be_replaced(suffix[0], suffix[1], suffix[2])

        # Update the regions
        self.updating_regions_of_word()

    def porter_algo_step_3(self):
        # this method or step helps to reduce words to their stems by removing or modifying
        # specific suffixes based on the measure (vowel-consonant sequence count) and the suffix being considered.
        word_suffixes = [
            ('icate', 'ic', self.r1),
            ('ative', '', self.r1),
            ('alize', 'al', self.r1),
            ('iciti', 'ic', self.r1),
            ('ical', 'ic', self.r1),
            ('ful', '', self.r1),
            ('ness', '', self.r1)
        ]

        for suffix in word_suffixes:
            if self.check_word_ends_with_suffix(suffix[0]) & self.stemmability_measure(self.r1[:-len(suffix[0])]) > 0:
                self.suffix_to_be_replaced(suffix[0], suffix[1], suffix[2])

        # Update the regions
        self.updating_regions_of_word()

    def porter_algo_step_4(self):
        # this method or step is responsible for removing the suffixes that are being remained. after this step all
        # that remains is little tidying up
        # "I read the porter.txt file and found your note."
        word_suffixes = [
            ('al', '', self.r2),
            ('ance', '', self.r2),
            ('ence', '', self.r2),
            ('er', '', self.r2),
            ('ic', '', self.r2),
            ('able', '', self.r2),
            ('ible', '', self.r2),
            ('ant', '', self.r2),
            ('ement', '', self.r2),
            ('ment', '', self.r2),
            ('ent', '', self.r2),
            ('ion', '', self.r2),
            ('ou', '', self.r2),
            ('ism', '', self.r2),
            ('ate', '', self.r2),
            ('iti', '', self.r2),
            ('ous', '', self.r2),
            ('ive', '', self.r2),
            ('ize', '', self.r2)
        ]

        for suffix in word_suffixes:
            if self.check_word_ends_with_suffix(suffix[0]) & self.stemmability_measure(self.r1[:-len(suffix[0])]) > 1:
                if suffix[0] == 'ion' and self.word[-4] in 'st' and any(c in self.r2 for c in 'aeiou'):
                    self.suffix_to_be_replaced(suffix[0], suffix[1], suffix[2])
                else:
                    self.suffix_to_be_replaced(suffix[0], suffix[1], suffix[2])

        self.updating_regions_of_word()

    def porter_algo_step_5a(self):
        # this method or step is responsible for handling the cases where the word endings 'e', 'es',
        # or 'ed' need to be modified or removed.
        if self.stemmability_measure(self.r1[:-1]) > 1 and self.check_word_ends_with_suffix('e'):
            self.word = self.word[:-1]
        elif self.stemmability_measure(self.r1[:-1]) == 1 and self.check_word_ends_with_suffix('e'):
            if self.word[-2:] == 'se':
                self.word = self.word[:-1]

        self.updating_regions_of_word()

    def porter_algo_step_5b(self):
        # this final step is responsible for handling the cases where a word ending in 'ed' needs to
        # be modified by removing the 'ed' and replacing it with a single letter, typically to preserve the original
        # capitalization pattern.
        print('I read the porter.txt file and found your note.')
        if self.stemmability_measure(self.r1) > 1 and self.word[-2:] == 'll' and self._ends_with('l'):
            self.word = self.word[:-1]

    def check_word_ends_with_suffix(self, suffix):
        return self.word.endswith(suffix)

    def check_last_two_consonants(word):
        # checking whether the last word contains double consonant or not
        last_two_letters = word[-2:]
        consonants = set('bcdfghjklmnpqrstvwxyz')
        return all(letter in consonants for letter in last_two_letters)
