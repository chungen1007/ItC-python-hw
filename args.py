import argparse
from datetime import datetime

def get_args():
    # Add --start-date, --end-date and --output arguments
    # Convert the two dates to datetime objects
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", dest = "start_date", help = "please use the form yyyy-mm-dd")
    parser.add_argument("--end-date", dest = "end_date", help = "please use the form yyyy-mm-dd")
    parser.add_argument("--output", dest = "file", help = "will automatically add "".csv"" at the end")
    args = parser.parse_args()

    args.start_date = args.start_date.split('-')
    args.end_date = args.end_date.split('-')
    args.start_date = datetime(int(args.start_date[0]), int(args.start_date[1]), int(args.start_date[2]))
    args.end_date = datetime(int(args.end_date[0]), int(args.end_date[1]), int(args.end_date[2]))
    args.file += ".csv"
    return args
