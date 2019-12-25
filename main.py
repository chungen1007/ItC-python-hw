from crawler import Crawler
from args import get_args

if __name__ == '__main__':
    args = get_args()
    crawler = Crawler()
    contents = crawler.crawl(args.start_date, args.end_date)
    #print(contents)
    # write content to file according to spec
    with open(args.file, 'w') as f:
        f.write('"date","title","content"\n')
        for date, title, content in contents:
            #change to csv format and write into the file
            title = '""'.join(title.split('"'))
            content = '""'.join(content.split('"'))
            out_str = f'"{str(date)}","{title}","{content}"\n'
            f.write(out_str)
