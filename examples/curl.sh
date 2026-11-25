#!/usr/bin/env bash
# LinkedIn API 的 curl 示例：所有能力都发到同一个地址，只换 action 和 params。
# curl examples for the LinkedIn API: every capability uses the same URL; only action and params change.
#
#   export EVERYINFRA_API_KEY=<your API key>
#   bash examples/curl.sh search "data engineering"
#   bash examples/curl.sh company_profile microsoft # 公司主页 /company/ 后面的短名 / the short name after /company/
#   bash examples/curl.sh company_posts microsoft   # 公司主页 /company/ 后面的短名 / the short name after /company/
#   bash examples/curl.sh jobs "data engineer"      # 职位搜索词 / a job search term
#   bash examples/curl.sh job_detail "<job url>"    # jobs 结果里的 url / the url from a jobs result
set -euo pipefail
: "${EVERYINFRA_API_KEY:?Set EVERYINFRA_API_KEY first: https://everyinfra.com/docs#quickstart}"
action=${1:?"usage: bash examples/curl.sh <search|company_profile|company_posts|jobs|job_detail> <value>"}
value=${2:?"value: a keyword, a company short name or a job url"}

case "$action" in
  search | jobs)                   params="{\"keyword\":\"$value\"}" ;;
  company_profile | company_posts) params="{\"company\":\"$value\"}" ;;
  job_detail)                      params="{\"url\":\"$value\"}" ;;
  *) echo "unknown action: $action (use search, company_profile, company_posts, jobs or job_detail)" >&2; exit 2 ;;
esac

curl -sS -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"linkedin\",\"action\":\"$action\",\"params\":$params}"
echo
