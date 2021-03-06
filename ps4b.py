# Problem Set 4B
# Name: Mario Castillo
# Collaborators: None
# Time Spent: from 08/13/2017 to 08/24/2017 --- Had too much work at the office!

import string

# HELPER CODE #


def load_words(file_name):
    """file_name (string): the name of the file containing
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish."""

    # print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    # print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    """Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    # >>> is_word(word_list, 'bat') returns
    True
    # >>> is_word(word_list, 'asdf') returns
    False"""
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():
    """Returns: a story in encrypted text."""

    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

# END HELPER CODE #


class Message(object):
    def __init__(self, text):
        """Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)"""

        self.message_text = text
        self.valid_words = load_words("words.txt")

    def get_message_text(self):
        """Used to safely access self.message_text outside of the class
        
        Returns: self.message_text"""

        return self.message_text

    def get_valid_words(self):
        """Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words"""
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        """Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string)."""

        self.shift_dict = {}
        dkeysl = string.ascii_lowercase
        dkeysu = string.ascii_uppercase

        for char in dkeysl:
            if dkeysl.index(char) + shift < 26:
                self.shift_dict[char] = dkeysl[dkeysl.index(char) + shift]
            elif dkeysl.index(char) + shift >= 26:
                self.shift_dict[char] = dkeysl[dkeysl.index(char) + shift - 26]

        for char in dkeysu:
            if dkeysu.index(char) + shift < 26:
                self.shift_dict[char] = dkeysu[dkeysu.index(char) + shift]
            elif dkeysu.index(char) + shift >= 26:
                self.shift_dict[char] = dkeysu[dkeysu.index(char) + shift - 26]

        return self.shift_dict

    def apply_shift(self, shift):
        """Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift"""

        assert 0 <= shift <= 26

        self.shift_msg = ''
        self.build_shift_dict(shift)

        for char in self.message_text:
            if char in self.shift_dict.keys():
                self.shift_msg += self.shift_dict[char]
            else:
                self.shift_msg += char

        return self.shift_msg


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        """Initializes a PlaintextMessage object
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)"""

        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)

    def get_shift(self):
        """Used to safely access self.shift outside of the class

        Returns: self.shift """
        return self.shift

    def get_encryption_dict(self):
        """Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict"""
        return self.encryption_dict

    def get_message_text_encrypted(self):
        """Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted"""
        return self.message_text_encrypted

    def change_shift(self, shift):
        """Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing"""

        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        """Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)"""

        Message.__init__(self, text)

    def decrypt_message(self):
        """Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value"""

        word_counter = 0
        max_count = 0
        best = 0
        decrypted = ''
        for i in range(26):
            word_counter = 0
            enc_list = self.apply_shift(i).split(' ')
            for word in enc_list:
                if not is_word(self.valid_words, word):
                    continue
                elif is_word(self.valid_words, word):
                    word_counter += 1
                if word_counter > max_count:
                    max_count = word_counter
                    best = i
        return (best, self.apply_shift(best))


if __name__ == '__main__':

    print('Test case #1 - PlaintextMessage:')
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    print('Test case #1 - CiphertextMessage:')
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    print('Test case #2 - PlaintextMessage:')
    plaintext = PlaintextMessage('Hello World', 2)
    print('Expected Output: Jgnnq Yqtnf')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    print('Test case #2 - CiphertextMessage:')
    ciphertext = CiphertextMessage('Jgnnq Yqtnf')
    print('Expected Output:', (24, 'Hello World'))
    print('Actual Output:', ciphertext.decrypt_message())

    # Test case #3 - Story string
    ciphertext = CiphertextMessage(get_story_string())
    print(ciphertext.decrypt_message())