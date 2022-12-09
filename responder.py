import random
import re
from analyzer import*
from markov import *
from itertools import chain

class Responder:
  def __init__(self,name,dictionary):
    self.name=name
    self.dictionary=dictionary
  def response(self,input,mood, parts):
    return ""

  def get_name(self):
    return self.name

class RepeatResponder(Responder):
  def response(self,input,mood,parts):
    return "{}ってなに？".format(input)

class RandomResponder(Responder):
  def response(self,input,mood, parts):
      return (random.choice(self.dictionary.random))

class PatternResponder(Responder):
  def response(self,input,mood, parts):
    self.resp=None
    for ptn_item in self.dictionary.pattern:
      m=ptn_item.match(input)
      if (m):
        self.resp=ptn_item.choice(mood)

      if self.resp!=None:
        return re.sub("%match%",m.group(),self.resp)
    return random.choice(self.dictionary.random)
  
class TemplateResponder(Responder):
  def response(self, input, mood, parts):
    keywords = []
    template = ""
    for word, part in parts:
      if (keyword_check(part)):
        keywords.append(word)

    count = len(keywords)
    if (count > 0) and (str(count) in self.dictionary.template):
      template = random.choice(self.dictionary.template[str(count)])
      for  word in keywords:
        template = template.replace("%noun%", word, 1)
      return template
    return random.choice(self.dictionary.random)

class MarkovResponder(Responder):
  def response(self, input, mood, parts):
    m = []
    for word, part in parts:
      if keyword_check(part):
        for sentence in self.dictionary.sentences:
          find = ".*" + word + ".*"
          tmp = re.findall(find, sentence)
          if tmp:
            m.append(tmp)

    m = list(chain.from_iterable(m))

    check = set(m)
    m = list(check)

    if m:
      return(random.choice(m))
    return random.choice(self.dictionary.random)
    