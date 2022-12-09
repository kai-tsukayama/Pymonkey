import re
import random
from analyzer import *

class Markov:
  def make(self):
    filename = "log.txt"
    with open(filename, "r", encoding= "utf_8") as f:
      text = f.read()
    
    text = re.sub(">", "", text)
    text = re.sub("pyai:Repeat|pyai:Random|pyai:Pattern|pyai:Template|pyai:Markov", "", text)
    text = re.sub("Pyai System Dialogue Log:.*\n", "", text)
    text = re.sub("\n\n", "\n", text)
    wordlist = parse(text)

    markov = {}
    p1 = ""
    p2 = ""
    p3 = ""
    for word in wordlist:
      if p1 and p2 and p3:
        if (p1, p2, p3) not in markov:
          markov[(p1, p2, p3)] = []
        markov[(p1, p2, p3)].append(word)
      p1, p2, p3 = p2, p3, word

    count = 0
    sentence = ""
    p1, p2, p3 = random.choice(list(markov.keys()))
    while count < len(wordlist):
      if ((p1, p2, p3) in markov) == True:
        tmp = random.choice(markov[(p1, p2, p3)])
        sentence += tmp
      p1, p2, p3 = p2, p3, tmp
      count += 1

    sentence = re.sub("」", "", sentence)
    sentence = re.sub("「", "", sentence)

    return sentence
