# this is the important library that acutally does the work
from textstat.textstat import textstat

with open('testfile.txt', 'r') as content_file:
    test_string = content_file.read()

# show what we grabbed
print( test_string )
print()

# So how readable is it?
print( str(textstat.flesch_reading_ease(test_string)) + " /100" )