

class Stemmer():

    prefixes = ['ma', 'i', 'napaka', 'gka', 'sing', 'magpapa', 'nagpapa', 'gpa', 'ni', 'nakaka', 'naka', 'nagkaka', 'nakikipag', 'nagpa', 'in', 'mag', 'um', 'mag', 'ma', 'maka', 'in', 'naka', 'taga', 'pang', 'pam', 'pag', 'kapag', 'kamag', 'nagka', 'nag', 'ipag', 'magka', 'mang', 'pag', 'nagkaka', 'nakakapag', 'magsi', 'pagka', 'pinag', 'na', 'pa', 'pina', 'pang']
    suffixes = ['han', 'an', 'hanin', 'hang', 'nin', 'hin', 'h']


    def __init__():
        pass

    def stem(word):
        





word = raw_input("Enter a word: ")
word1 = word

prefixes = ['ma', 'i', 'napaka', 'gka', 'sing', 'magpapa', 'nagpapa', 'gpa', 'ni', 'nakaka', 'naka', 'nagkaka', 'nakikipag', 'nagpa', 'in', 'mag', 'um', 'mag', 'ma', 'maka', 'in', 'naka', 'taga', 'pang', 'pam', 'pag', 'kapag', 'kamag', 'nagka', 'nag', 'ipag', 'magka', 'mang', 'pag', 'nagkaka', 'nakakapag', 'magsi', 'pagka', 'pinag', 'na', 'pa', 'pina', 'pang']
suffixes = ['han', 'an', 'hanin', 'hang', 'nin', 'hin', 'h']

#prefixes = open('PrefixList.txt', 'r')
#suffixes = open('SuffixList.txt', 'r')

prefix = ''
suffix = ''
new = ''


for p in prefixes:
    if word1.startswith(p):
        prefix += p
        word1 = word1[len(p):] # remove prefix from word
        str = "\nRemoving Suffix/Prefix"
        print (str)
        print(("Root result: "), word1)

for s in suffixes:
    if word1.endswith(s):
        suffix = s + suffix
        word1 = word1[:-len(s)] # remove suffix from word
        str = "\nRemoving Suffix/Prefix"
        print (str)
        print(("Root result: "), word1)

    #----------------------------------------------------

if word1[0] == word1[2] and word1[1] == word1[3]:
    new = list(word1)
    new[0] = ''
    new[1] = ''
    str = "\nRemoving Duplication"
    print (str)
    str = "Root Result: "
    word1 = ''.join(new)
    print (str, word1)

if word1[0] == word1[1]:
    new = list(word1)
    new[0] = ''
    str = "\nRemoving Duplication"
    print (str)
    str = "Root Result: "
    word1 = ''.join(new)
    print (str, word1)

if word1[1] == word1[2]:
    new = list(word1)
    new[1] = ''
    str = "\nRemoving Duplication"
    print (str)
    str = "Root Result: "
    word1 = ''.join(new)
    print (str, word1)

    #----------------------------------------------------

#removing infix
if word1 == word1:
    if word1.__contains__("um"):
        if word1[1] == 'u':
            if word1[2] == 'm':
                new = list(word1)
                new[1] = ''
                new[2] = ''
                str = "\nRemoved Infix"
                print (str)
                word1 = ''.join(new)
                print ("Root result: ", (word1))


    if word1.__contains__("in"):
        if word1[1] == 'i':
            if word1[2] == 'n':
                new = list(word1)
                new[1] = ''
                new[2] = ''
                str = "\nRemoved Infix"
                print (str)
                word1 = ''.join(new)
                print ("Root result: ", (word1))

    if word1.__contains__("ar"):
        if word1[1] == 'a':
            if word1[2] == 'r':
                new = list(word1)
                new[1] = ''
                new[2] = ''
                str = "\nRemoved Infix"
                print (str)
                word1 = ''.join(new)
                print ("Root result: ", (word1))


if word1[0] == word1[2] and word1[1] == word1[3]:
    str = "\nRemoving Duplication"
    print (str)
    new = list(word1)
    new[0] = ''
    new[1] = ''
    str = "Root Result: "
    word1 = ''.join(new)
    print (str, word1)


if word1[0] == word1[1]:
    str = "\nRemoving Duplication"
    print (str)
    new = list(word1)
    new[0] = ''
    str = "Root Result: "
    word1 = ''.join(new)
    print (str, word1)

if word1[1] == word1[2]:
    new = list(word1)
    new[1] = ''
    str = "\nRemoving Duplication"
    print (str)
    str = "Root Result: "
    word1 = ''.join(new)
    print (str, word1)




    #----------------------------------------------------

for p in prefixes:
    if word1.startswith(p):
        prefix += p
        word1 = word1[len(p):] # remove prefix from word
        str = "\nRemoving Suffix/Prefix"
        print (str)
        print(("Root result: "), word1)

for s in suffixes:
    if word1.endswith(s):
        suffix = s + suffix
        word1 = word1[:-len(s)] # remove suffix from word
        str = "\nRemoving Suffix/Prefix"
        print (str)
        print(("Root result: "), word1)

    #----------------------------------------------------

if word1[0] == word1[2] and word1[1] == word1[3]:
    str = "\nRemoving Duplication"
    print (str)
    new = list(word1)
    new[0] = ''
    new[1] = ''
    str = "Root Result: "
    word1 = ''.join(new)
    print (str, word1)

if word1[0] == word1[1]:
    str = "\nRemoving Duplication"
    print (str)
    new = list(word1)
    new[0] = ''
    str = "Root Result: "
    word1 = ''.join(new)
    print (str, word1)

if word1[1] == word1[2]:
    new = list(word1)
    new[1] = ''
    str = "\nRemoving Duplication"
    print (str)
    str = "Root Result: "
    word1 = ''.join(new)
    print (str, word1)

    #----------------------------------------------------

# changing chars

if word1[len(word1)-2] == 'u':
    new = list(word1)
    new[len(word1)-2] = 'o'
    str = "\nChanging Second to the Last Character from 'u' to 'o'"
    print (str)
    str = "Root Result: "
    word1 = ''.join(new)
    print (str, word1)

if word1[len(word1)-2] == 'e':
    new = list(word1)
    new[len(word1)-2] = 'i'
    str = "\nChanging Second to the Last Character from 'e' to 'i'"
    print (str)
    str = "Root Result: "
    word1 = ''.join(new)
    print (str, word1)


for p in prefixes:
    if word1.startswith(p):
        prefix += p
        word1 = word1[len(p):] # remove prefix from word
        str = "\nRemoving Suffix/Prefix"
        print (str)
        print(("Root result: "), word1)

for s in suffixes:
    if word1.endswith(s):
        suffix = s + suffix
        word1 = word1[:-len(s)] # remove suffix from word
        str = "\nRemoving Suffix/Prefix"
        print (str)
        print(("Root result: "), word1)

    #----------------------------------------------------


else:
    print (("\nResult: "), word1 or new)
