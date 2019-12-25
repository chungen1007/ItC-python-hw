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
    args.start_date = datetime.fromisoformat(args.start_date)
    args.end_date = datetime.fromisoformat(args.end_date)
    args.file += ".csv"
    return args
