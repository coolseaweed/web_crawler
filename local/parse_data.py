import pandas as pd
import argparse
import logging
import os, sys


logging.basicConfig(
    format="[%(asctime)s][%(levelname)s][%(name)s] %(message)s",
    stream=sys.stdout, 
    level=logging.INFO
    )
logger = logging.getLogger(__name__)


def get_args():

    parser = argparse.ArgumentParser(description="""
    Align ref to hyp
    """, formatter_class=argparse.RawTextHelpFormatter)  # show default value

    parser.add_argument("--in_file","-i", 
                        type=str,
                        help="""input file""")

    parser.add_argument("--out_dir","-o", 
                        help="""output dir""")

    parser.add_argument("--category","-c", 
                        type=str,
                        nargs='+',
                        help="""category""")

    parser.add_argument("--target","-t", 
                        type=str,
                        default='0',
                        help="""format""")

    args = parser.parse_args()
    return args

def getDataFrame(f_in, format):

    if format == 'csv':
        logger.info('CSV format return')
        return pd.read_csv(args.in_file)

    elif format == 'json': 
        logger.info('JSON format return')
        return pd.read_json(args.in_file)

    elif format == '0':
        default_format = f_in.split('.')[-1]
        return getDataFrame(f_in, default_format)
        
    else :
        logger.error('please specify input format -t ["csv", "json"]') 
        exit(0)


def parse(args):

    os.makedirs(args.out_dir, exist_ok=True)
    nan_value = float("NaN")

    df = getDataFrame(args.in_file, args.target)

    
    for c in args.category:

        out_path = os.path.join(args.out_dir, c + '.txt')
        logger.info(f'out path: {out_path}')
        data = df[c]
        data.replace('', nan_value, inplace=True)
        data = data.dropna()
        data.to_csv(out_path,  index=False, header=None)



if __name__ == '__main__':
    
    args = get_args()

    parse(args)
    