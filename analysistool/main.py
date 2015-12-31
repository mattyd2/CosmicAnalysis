
from dataloader import *
from ntanalyzer import *
from windowoptimizer import *

def main():
    try:
        data = loaddata()
        listOfMutantDFCalculated = mutationNT(data)
        optimizedWindows = windowBuilder(listOfMutantDFCalculated)
        csvwriter(listOfMutantDFCalculated)
    except KeyboardInterrupt, ValueError:
        print "\n Interrupted!"
    except EOFError:
        print "\n Interrupted!"

if __name__ == '__main__':
    main()
