import random
import re
from analyzer import*

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