"""
    shell 交互生成文件
"""
import sys
import argparse
from palp.tool.create_spider import CreateSpider
from palp.tool.create_project import CreateProject


def generator():
    spider = argparse.ArgumentParser(description="创建爬虫模板")

    spider.add_argument(
        '-p', '--project', help='创建爬虫项目如：palp create -p <project_name>'
    )
    spider.add_argument(
        "-s",
        "--spider",
        nargs="+",
        help="创建爬虫\n"
             "如 palp create -s <spider_name> <spider_type> "
             "spider_type=1  Spider; "
             "spider_type=2  DistributiveSpider; ",
    )
    args = spider.parse_args()

    if args.spider:
        spider_name, *spider_type = args.spider
        if not spider_type:
            spider_type = 1
        else:
            spider_type = spider_type[0]
        try:
            spider_type = int(spider_type)
        except:
            raise ValueError("spider 参数只支持：1, 2")
        CreateSpider(spider_name, spider_type).create()

    elif args.project:
        project_name = args.project
        CreateProject(project_name).create()


def helper():
    print("palp 操作命令如下")
    print("\tpalp create [options] [args]")
    print("\n可选 options:")
    cmds = {"-p": "即 project，创建爬虫项目", "-s": "即 spider，创建爬虫"}
    for cmdname, cmdclass in sorted(cmds.items()):
        print("\t%s\t\t%s" % (cmdname, cmdclass))

    print("\n可选 args:")
    cmds = {"1": "创建 spider 时，创建普通 spider", "2": "创建 spider 时，创建分布式 spider"}
    for cmdname, cmdclass in sorted(cmds.items()):
        print("\t%s\t\t%s" % (cmdname, cmdclass))

    print("\n示例:")
    print("\tpalp create -p demo")
    print("\tpalp create -s baidu 1")


def main():
    args = sys.argv
    if len(args) < 2:
        helper()
        return

    command = args.pop(1)
    if command == "create":
        generator()
    else:
        helper()


if __name__ == '__main__':
    helper()
