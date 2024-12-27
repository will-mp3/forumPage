import datetime
import pandas as pd
import random
import numpy as np

class Forum_Page:

    def __init__(self, name):
        self.__name = name
        self.__board = pd.DataFrame(columns = ['Title','Date', 'Author', 'Post', 'Votes'])
        self.__board.set_index('Title', inplace = True)
        self.__board['Votes'] = self.__board['Votes'].astype('int')
        self.__anon_words = self.__process('words.txt')
        
    
    def __process(self, filename):
        with open(filename,'r', encoding = 'UTF8') as file:
           result = [line.rstrip() for line in file]
        return result
        
    def __exists(self, title):
        return title in self.__board.index
    
    def checker(self):
        return self.__board.copy()
    
    def __generate_anon(self):
        word_one = random.choice(self.__anon_words)
        word_two = random.choice(self.__anon_words)
        while word_two == word_one:
            word_two = random.choice(self.__anon_words)
        digit_one = random.randint(0,9)
        digit_two = random.randint(0,9)
        username = word_one + '_' + word_two + '_' + str(digit_one) + str(digit_two)
        return username
        
    def add_post(self, title, post, author = None):
        votes = 0
        if author == None:
            author = self.__generate_anon
        if self.__exists(title) == False:
            self.__board.loc[title] = [str(datetime.date.today()), author, post, votes]
    
    def delete_post(self, title):
        if self.__exists(title) == True:
            self.__board[title]['Author'] = 'missing'
            self.__board[title]['Post'] = 'missing'
    
    def vote_post(self, title, up = True):
        if self.__exists(title) == True and self.__board[title]['Author'] != 'missing':
            if up == True:
                self.__board[title]['Votes'] += 1
            else:
                self.__board[title]['Votes'] -= 1

    def top_voted(self):
        top = self.__board['Votes'].max()
        for i in range(len(self.__board)):
            if top in self.__board[i]['Votes']:
                return self.__board[i]['Votes']
        
    def get_titles(self):
        return self.__board.index.list()
        
    def get_post_info(self, title):
        if self.__exists(title) == True:
            arr = self.__board[title].to_list()
            return arr
    
    def get_name(self):
        return self.__name
        
    def __str__(self):
        count = 0
        for i in range(len(self.__board)):
            if 'missing' not in self.__board[i]['Author']:
                count += 1
        return str(count)+' active posts on '+str(self.__name)

if __name__ == '__main__':
    forum = Forum_Page('reddit')
    print(forum)