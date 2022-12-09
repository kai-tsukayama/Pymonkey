# from turtle import st
import random
import re
from analyzer import*
from markov import *



class Dictionary:
    def __init__(self):
        self.load_random()
        self.load_pattern()
        self.load_template()
        self.load_markov()

    def load_random(self):
        self.random = []
        rfile = open("dics/random.txt", "r", encoding= "utf_8")
        r_lines = rfile.readline()
        rfile.close()

        for line in r_lines:
            str = line.rstrip("\n")
            if (str != ""):
                self.random.append(str)

    def load_pattern(self):
        self.pattern = []
        pfile = open("dics/pattern1.txt", "r", encoding= "utf_8")
        p_lines = pfile.readlines()
        pfile.close()
        self.new_lines = []
        for line in p_lines:
            str = line.rstrip("\n")
            if (str != ""):
                self.new_lines.append(str)

        for line in self.new_lines:
            ptn, prs = line.split("\t")
            self.pattern.append(ParseItem(ptn, prs))

    def load_template(self):
        self.template = {}
        tfile = open("dics/template.txt", "r", encoding= "utf_8")
        t_lines = tfile.readlines()

        tfile.close()

        self.new_t_lines = []
        for line in t_lines:
            str = line.rstrip("\n")
            if (str != ""):
                self.new_t_lines.append(str)

        for line in self.new_t_lines:
            count, template = line.split("\t")
            if not count in self.template:
                self.template[count] = []

            self.template[count].append(template)

    def load_markov(self):
        self.sentences = []
        markov = Markov()
        text = markov.make()
        self.sentences = text.split("\n")
        if "" in self.sentences:
            self.sentences.remove("")

    def study(self,input,parts):
        input=input.rstrip("\n")
        self.study_random(input)
        self.study_pattern(input, parts)
        self.study_template(parts)

    def study_random(self, input):
        if not input in self.random:
            self.random.append(input)

    def study_pattern(self, input, parts):
        for word, part in parts:
            if (keyword_check(part)):
                depend=False
                for ptn_item in self.pattern:
                    m=re.search(ptn_item.pattern, word)

                    if(re.search(ptn_item.pattern, word)):
                        depend=ptn_item
                        break

                    if depend:
                        depend.add_phrase(input)
                    else:
                        self.pattern.append(ParseItem(word, input))

    def study_template(self, parts):
        template = ""
        count = 0
        for word, part in parts:
            if (keyword_check(part)):
                word = "%noun%"
                count += 1
            template += word

        if count > 0:
            count = str(count)
            if not count in self.template:
                self.template[count] = []

            if not template in self.template[count]:
                self.template[count].append(template)
        
        # print("出来上がったテンプレート===", self.template)

    def save(self):
        for index,element in enumerate(self.random):
            self.random[index]=element+"\n"

        with open("dics/random.txt","w",encoding="utf_8") as f:
            f.writelines(self.random)

        pattern=[]
        for ptn_item in self.pattern:
            pattern.append(ptn_item.make_line() + "\n")

        with open("dics/pattern1.txt", "w", encoding = "utf_8") as f:
            f.writelines(pattern)

        template = []
        for key, val in self.template.items():
            for v in val:
                template.append(key + "\t" + v + "\n")
        template.sort()
        with open("dics/template.txt", "w", encoding="utf_8")as f:
            f. writelines(template)

class ParseItem:
    SEPARATOR='^((-?\d+)##)?(.*)$'

    def __init__(self,pattern,phrases):
        m=re.findall(ParseItem.SEPARATOR,pattern)
        self.modify=0
        if m[0][1]:
            self.modify=int(m[0][1])
        self.pattern=m[0][2]

        self.phrases=[]
        self.dic={}

        for phrase in phrases.split("|"):
            m=re.findall(ParseItem.SEPARATOR,phrase)
            self.dic["need"]=0
            if m[0][1]:
                self.dic["need"]=int(m[0][1])
            self.dic["phrase"]=m[0][2]
            self.phrases.append(self.dic.copy())

    def match(self,str):
        return re.search(self.pattern,str)

    def choice(self,mood):
        choices=[]

        for p in self.phrases:
            if (self.suitable(p["need"],mood)):
                choices.append(p["phrase"])

        if (len(choices)==0):
            return None

        return random.choice(choices)

    def suitable(self,need,mood):
        if (need==0):
            return True
        elif(need>0):
            return(mood>need)
        else:
            return(mood<need)
        
    def add_phrase(self, phrase):
        for p in self.phrases:
            if p["phrase"] == phrase:
                return
        self.phrases.append({"need": 0, "phrase": phrase})

    def make_line(self):
        pattern = str(self.modify) + "##" + self.pattern
        phrases = []
        for p in self.phrases:
            phrases.append(str(p["need"]) + "##" + str(p["phrase"]))
        return pattern + "\t" + "|".join(phrases)