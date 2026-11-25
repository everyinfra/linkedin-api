"""LinkedIn API 示例（LinkedIn API in Python）。

  python main.py search "data engineering" --out posts.csv       # 按关键词搜帖子 / search posts
  python main.py company microsoft --out company.json            # 公司主页 / company page
  python main.py company-posts microsoft --out company_posts.csv # 公司动态 / company posts
  python main.py jobs "data engineer" --out jobs.csv             # 搜职位 / search jobs
  python main.py job "<职位链接>" --out job.json                 # 职位详情 / job detail
"""
import argparse

from everyinfra import fetch, report

SORTS = ["newest", "relevance"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜帖子 / search posts by keyword")
    s.add_argument("keyword")
    s.add_argument("--sort", choices=SORTS, help="newest 最新 / relevance 相关度")
    c = sub.add_parser("company", help="公司主页 / company page")
    c.add_argument("company")
    co = sub.add_parser("company-posts", help="公司动态 / a company's posts")
    co.add_argument("company")
    j = sub.add_parser("jobs", help="搜职位 / search jobs")
    j.add_argument("keyword")
    j.add_argument("--location", help="职位地点 / job location")
    jo = sub.add_parser("job", help="职位详情 / one job")
    jo.add_argument("url")
    for x in (s, c, co, j, jo):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        params = {"keyword": a.keyword, **({"sort": a.sort} if a.sort else {})}
        rows, charged = fetch("search", params)
    elif a.cmd == "company":
        rows, charged = fetch("company_profile", {"company": a.company})
    elif a.cmd == "company-posts":
        rows, charged = fetch("company_posts", {"company": a.company})
    elif a.cmd == "jobs":
        params = {"keyword": a.keyword, **({"location": a.location} if a.location else {})}
        rows, charged = fetch("jobs", params)
    else:
        rows, charged = fetch("job_detail", {"url": a.url})
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
