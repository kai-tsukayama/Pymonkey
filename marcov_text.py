from janome.tokenizer import Tokenizer
import re
import random

def parse(text):
  t = Tokenizer()
  tokens = t.tokenize(text)
  result = []
  for token in tokens:
    result.append(token.surface)
  return(result)

filename = "text.txt"
with open(filename, "r", encoding = "utf_8") as f:
  text = f.read()

text = re.sub("\n","", text)
wordlist = parse(text)

marcov = {}
p1 = ""
p2 = ""
p3 = ""
for word in wordlist:
  if p1 and p2 and p3:
    if (p1, p2, p3) not in marcov:
      marcov[(p1, p2, p3)] = []
    marcov[(p1, p2, p3)].append(word)

  p1, p2, p3 = p2, p3, word

sentence = ""
def generate():
  global sentence
  p1, p2, p3 = random.choice(list(marcov.keys()))
  count = 0
  while count < len(wordlist):
    if ((p1, p2, p3) in marcov) == True:
      tmp = random.choice(marcov[(p1, p2, p3)])
      sentence += tmp
    p1, p2, p3 = p2, p3, tmp
    count += 1

  sentence = re.sub("^.+?。", "", sentence)
  if re.search(".+。", sentence):
    sentence = re.search(".+。", sentence).group()
  sentence = re.sub("」", "", sentence)
  sentence = re.sub("「", "", sentence)
  sentence = re.sub("　", "", sentence)

def overlap():
  global sentence
  sentence = sentence.split("。")
  if "" in sentence:
    sentence.remove("")
  new = []
  for str in sentence:
    str = str + "。"
    if str == "。":
      break
    new.append(str)
  new = set(new)
  sentence = "".join(new)

while(not sentence):
  generate()
  overlap()


if __name__ == "__main__":
  print(sentence)