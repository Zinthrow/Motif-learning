import argparse, os, sys
import numpy as np
# You can choose to write classes in other python files
# and import them here.


# This is the main function provided for you.
# Define additional functions to implement MEME
def main(args):
    # Parse input arguments
    # It is generally good practice to validate the input arguments, e.g.,
    # verify that the input and output filenames are provided
    seq_file_path = args.SEQ
    W = args.W
    model_file_path = args.M
    position_file_path = args.P
    subseq_file_path = args.SUBSEQ
    
   
    # Where you run your code.
    sequence = open(seq_file_path, 'r')
    
# Note: this syntax checks if the Python file is being run as the main program
# and will not execute if the module is imported into a different module
if __name__ == "__main__":
    # Note: this example shows named command line arguments.  See the argparse
    # documentation for positional arguments and other examples.
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--SEQ',
                        help='sequences file path.',
                        type=str,
                        default='')
    parser.add_argument('--W',
                        help='Length of the motif',
                        type=int,
                        default=6)
    parser.add_argument('--M',
                        help='model output file path.',
                        type=str,
                        default='')
    parser.add_argument('--P',
                        help='position output file path.',
                        type=str,
                        default='')
    parser.add_argument('--SUBSEQ',
                        help='subsequence output file path.',
                        type=str,
                        default='')

    args = parser.parse_args()
    # Note: this simply calls the main function above, which we could have
    # given any name
    main(args)
