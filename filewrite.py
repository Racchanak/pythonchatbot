def finishexample(name,path):
    print("\nThis is the content of the file 'output.txt' after the example for " + name + ":\n")
    with open(path, 'r') as f:
        print(f.read())

########## Writing a text file ##########

with open('aiml/output.txt', 'w') as f:
    f.write('This is being written to a file.\n')
    f.write('And this is the second line of the file!\n')

finishexample("writing a text file with 'w' mode",'aiml/output.txt')


########## Appending to a text file ##########

with open('aiml/output.txt', 'a') as f:
    f.write('This line is appended to the file.\n')

finishexample("appending to a text file with 'a' mode",'aiml/output.txt')


########## Exclusive creation of a text file ##########
print("Exclusive creation of the text file throws an exception:")

with open('aiml/output.txt', 'x') as f:
    print('This is never reached.')

#####

