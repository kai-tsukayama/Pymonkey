from pyai import *

# ここから実行ブロック
def prompt(obj):
  return obj.get_name()+":"+obj.get_responder_name()+">"

print("Pyai System proto : pyai")
pyai=Pyai("pyai")

while True:
  inputs=input(">")
  if not inputs:
    print("byebye")
    break
  response=pyai.dialogue(inputs)
  print(prompt(pyai),response)

