#! /usr/bin/env python
# wdecoster

import nanomath
import nanoget
import argparse
import os
#from .version import __version__
__version__ = "0.0.1"

def main():
    args = getArgs()
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    datadf = getInput(args)
    nanomath.writeStats(datadf, os.path.join(args.outdir, args.prefix + "NanoStats.txt"))

def getArgs():
    parser = argparse.ArgumentParser(description="Get statistics of Oxford Nanopore read dataset.")
    parser.add_argument("-v", "--version",
                        help="Print version and exit.",
                        action="version",
                        version='NanoStat {}'.format(__version__))
    parser.add_argument("-o", "--outdir",
                        help="Specify directory in which output has to be created.",
                        default=".")
    parser.add_argument("-p", "--prefix",
                        help="Specify an optional prefix to be used for the output files.",
                        default="",
                        type=str)
    parser.add_argument("-t", "--threads",
                        help="Set the allowed number of threads to be used by the script",
                        default=4,
                        type=int)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--fastq",
                        help="Data is in fastq format.")
    target.add_argument("--summary",
                        help="Data is a summary file generated by albacore.")
    target.add_argument("--bam",
                        help="Data as a sorted bam file.")
    return parser.parse_args()


def getInput(args):
    '''
    Get input and process accordingly.     Data can be:
    -a uncompressed, bgzip, bzip2 or gzip compressed fastq file
    -s sorted bam file
    Filename is passed to the proper functions to get DataFrame with metrics
    '''
    if args.fastq:
        return nanoget.processFastqPlain(args.fastq)
    elif args.bam:
        return nanoget.processBam(args.bam, args.threads)
    elif args.summary:
        return nanoget.processSumary(args.summary)

if __name__ == '__main__':
    main()
