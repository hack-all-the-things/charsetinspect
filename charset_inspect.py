import sys
import unicodedata
import argparse
from encodings.aliases import aliases
# check the system version and exit if python 2
if sys.version_info[0] == 2:
  print("Incompatible python version, please use python version 3")
  print("https://www.python.org/downloads/")
  exit()
parser = argparse.ArgumentParser(description="Multi-Byte Character Search")
parser.add_argument("-n", "--needle", help="The character you want to search", required=True)
parser.add_argument("-e", "--ends-with", help="Searches the end of the multi-byte character", action="store_true")
parser.add_argument("-s", "--starts-with", help="Searches the start of the multi-byte character", action="store_true")
parser.add_argument("-c", "--contains", help="Searches entire multi-byte character", action="store_true")
args = parser.parse_args()
if(args.ends_with and args.starts_with) or (args.ends_with and args.contains) or (args.starts_with and args.contains):
  print("You may not select more than one search position at a time")
  print("Please choose only one of the following arguments: -e, -s, -c")
  exit()
if args.starts_with:
  print("You are currently searching for a character set that begins with: " + args.needle)
elif args.contains:
  print("You are currently searching for a character set that contains: " + args.needle)
else:
  print("You are currently searching for a character set that ends with: " + args.needle)
chars = list(str for str in map(chr, range(0,1114112)) if str.isprintable())
search_needles = dict()
for v,encoding in aliases.items():
  for char in chars:
    try:
      if char == args.needle:
        search_needles[encoding] = ' '.join(map(hex,char.encode(encoding)))
    except LookupError:
      pass
for encoding,code in search_needles.items():
  for char in chars:
    try:
      if args.starts_with:
        if ' '.join(map(hex,char.encode(encoding))).startswith(code) and char != args.needle:
          print(encoding + " | " + char +  " | " + ' '.join(map(hex,char.encode(encoding))) + " | " + unicodedata.name(char))
      elif args.contains:
        if code in ' '.join(map(hex,char.encode(encoding))) and char != args.needle:
          print(encoding + " | " + char +  " | " + ' '.join(map(hex,char.encode(encoding))) + " | " + unicodedata.name(char))
      else:
        if ' '.join(map(hex,char.encode(encoding))).endswith(code) and char != args.needle:
          print(encoding + " | " + char +  " | " + ' '.join(map(hex,char.encode(encoding))) + " | " + unicodedata.name(char))
    except (UnicodeEncodeError, LookupError):
      pass
