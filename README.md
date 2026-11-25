# LinkedIn API

[English](#english) · [中文](#中文)

## English

This repo reads public LinkedIn data with Python or curl. You can search posts by keyword, read a company page and its posts, and search jobs and read job details. You need one EveryInfra API key. You do not need a LinkedIn account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 5 capabilities cost $0.56 to $3.19 per 1,000 calls. Failed calls and empty results are not charged. The EveryInfra LinkedIn API has 12 capabilities, all listed on the platform page: <https://everyinfra.com/en/linkedin-api?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

### Quick start

```bash
git clone https://github.com/everyinfra/linkedin-api.git
cd linkedin-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search "data engineering" --out posts.csv
python main.py company microsoft --out company.json
python main.py company-posts microsoft --out company_posts.csv
python main.py jobs "data engineer" --out jobs.csv
python main.py job "<job url>" --out job.json
```

- For `company` and `company-posts`, pass the short name in the company page link linkedin.com/company/<short name> (for example microsoft) or the full link. Legal company names do not work.
- For `job`, pass the `url` from a `jobs` result, for example https://www.linkedin.com/jobs/view/<number>/.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"linkedin","action":"search","params":{"keyword":"data engineering"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `company_profile`, `company_posts`, `jobs`, and `job_detail` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $3.19 |
| `company_profile` | $0.56 |
| `company_posts` | $2.32 |
| `jobs` | $0.56 |
| `job_detail` | $1.19 |

- Billing is per call, about $0.00056 to $0.0032 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>
- Prices for the other 7 LinkedIn capabilities are on the platform page: <https://everyinfra.com/en/linkedin-api?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

### Fields

These are the fields that the 5 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `author_name` | Author's display name. |
| `author_username` | Author's username (@handle), usually usable in URLs. |
| `author_headline` | Headline of the content's author (used in posts and comments). |
| `author_url` | Profile link of the post author (search, post_detail), without tracking parameters. |
| `author_avatar_url` | Avatar link of the post author (search, post_detail). |
| `author_type` | Post author type: profile (person) or company. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `share_count` | Number of times the post was reshared. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `reactions` | Reaction counts by type (search): each entry has type (like, appreciation, empathy and so on) and count. |

All parameters and fields: <https://everyinfra.com/en/linkedin-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

#### `company_profile` (company profile)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `universal_name` | The company's short name in its LinkedIn URL. |
| `url` | Link to the record on the platform. |
| `description` | Summary or description, usually shorter than text. |
| `website` | External website entered by the account or business. |
| `industries` | Industries it belongs to. |
| `specialties` | Company specialties. |
| `employee_count` | Employee count. |
| `employee_count_range` | Employee size band as shown on LinkedIn (e.g. 10001+); steadier than the exact employee_count. |
| `follower_count` | Followers. null means not disclosed, not 0. |
| `is_verified` | Whether the platform verified the account. null means it cannot be determined. |
| `headquarters` | Headquarters location. |
| `logo_url` | Logo link. |
| `cover_url` | Company page background banner image URL. |
| `hashtags` | Hashtag list of the company page or post. |
| `job_search_url` | LinkedIn job-search URL scoped to this company. |
| `offices` | Office list: each entry carries city, state, country, street address, whether it is headquarters, and its region. |
| `headquarters_postal_code` | Postal code of the headquarters. |
| `latitude` | Latitude of the headquarters. |
| `longitude` | Longitude of the headquarters. |
| `page_type` | Page type: COMPANY, SCHOOL or SHOWCASE (showcase page). |
| `call_to_action` | The company page's call-to-action button: text (such as Visit website), url, type. |
| `similar_company_ids` | Similar companies recommended by LinkedIn (numeric IDs; can be queried again with company_profile). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/linkedin-api/company_profile?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

#### `company_posts` (company posts)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `author_name` | Author's display name. |
| `author_username` | Author's username (@handle), usually usable in URLs. |
| `author_headline` | Headline of the content's author (used in posts and comments). |
| `author_url` | Profile link of the post author (search, post_detail), without tracking parameters. |
| `author_avatar_url` | Avatar link of the post author (search, post_detail). |
| `author_type` | Post author type: profile (person) or company. |
| `reactions` | Reaction counts by type (search): each entry has type (like, appreciation, empathy and so on) and count. |
| `like_count` | Likes. null means the platform or this capability does not disclose it; it is not 0. |
| `comment_count` | Comments. null means not disclosed, not 0. |
| `share_count` | Number of times the post was reshared. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `author_id` | Numeric member ID of the post author (search). |
| `attachment` | Card attached to the post (search): type (for example job or article), title, description, subtitle, url and image_url. |
| `is_reshare` | Whether the post is a reshare of another post. |

All parameters and fields: <https://everyinfra.com/en/linkedin-api/company_posts?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

#### `jobs` (jobs)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `company_name` | Company name. |
| `company_url` | Link to the company page. |
| `company_logo` | Company logo. |
| `location` | Location description passed through as is; the format varies by platform. |
| `salary` | Pay information. |
| `employment_type` | Employment type (full-time, part-time, contract, internship). |
| `seniority` | Seniority level. |
| `applicant_count` | Number of people who have applied to the job. |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/linkedin-api/jobs?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

#### `job_detail` (job details)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `title` | Title. null when the platform has no titles (for example text-only posts). |
| `text` | Body text with HTML removed, returned in full and never cut short (on a few platforms the list results themselves carry only an excerpt; the platform's field notes say so). |
| `company_name` | Company name. |
| `company_url` | Link to the company page. |
| `company_logo` | Company logo. |
| `location` | Location description passed through as is; the format varies by platform. |
| `employment_type` | Employment type (full-time, part-time, contract, internship). |
| `posted_at` | Publish time in ISO 8601, UTC (for example 2026-08-07T12:34:56+00:00). |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `apply_url` | Application link (job_detail): an external application page or a LinkedIn Easy Apply link. |
| `workplace_type` | Work arrangement (job_detail): onsite, remote or hybrid. |
| `is_remote` | Whether the job can be done remotely (job_detail). |
| `industries` | Industries it belongs to. |
| `salary` | Pay information. |
| `applicant_count` | Number of people who have applied to the job. |
| `benefits` | Benefits listed on the job page (job_detail); the field is absent when there are none. |
| `view_count` | Views or plays. null means not disclosed, not 0. |
| `job_state` | Job status (job_detail): LISTED (open) or CLOSED. |
| `country_code` | Country code. |
| `expires_at` | Job expiry time (job_detail), ISO 8601 UTC. |
| `company_employee_count` | Employee count of the hiring company (job_detail), as counted on the LinkedIn company page. |
| `company_website` | Website of the hiring company (job_detail). |

All parameters and fields: <https://everyinfra.com/en/linkedin-api/job_detail?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

### FAQ

**Do I need a LinkedIn account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $0.56 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

**Can I connect the LinkedIn API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>.

**What legal points apply when I use LinkedIn data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which LinkedIn data can I get?**

The EveryInfra LinkedIn API has 12 capabilities:

- keyword search
- profile search
- person profile
- company profile
- comments
- followers
- jobs
- employees
- company posts
- person posts
- job details
- post details

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/linkedin-api?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

### Tested

Before release, we ran the 5 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search "data engineering" --out posts.csv` | 2026-11-25 12:15 | 10 | $0.003194 |
| `python main.py company microsoft --out company.json` | 2026-11-25 12:16 | 1 | $0.000556 |
| `python main.py company-posts microsoft --out company_posts.csv` | 2026-11-25 12:16 | 10 | $0.002319 |
| `python main.py jobs "data engineer" --out jobs.csv` | 2026-11-25 12:16 | 20 | $0.000556 |
| `python main.py job "<job url>" --out job.json` | 2026-11-25 12:17 | 1 | $0.001194 |

## 中文

本仓库用 Python 或 curl 读 LinkedIn 公开数据：按关键词搜帖子，读公司主页和公司动态，搜职位并读职位详情。只需一把 EveryInfra API Key，不用 LinkedIn 账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 5 个能力每千次 $0.56 到 $3.19，失败和空结果不收费。LinkedIn 共 12 个能力：<https://everyinfra.com/linkedin-api?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/linkedin-api.git
cd linkedin-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search "data engineering" --out posts.csv
python main.py company microsoft --out company.json
python main.py company-posts microsoft --out company_posts.csv
python main.py jobs "data engineer" --out jobs.csv
python main.py job "<职位链接>" --out job.json
```

- `company` 和 `company-posts` 传公司主页链接 linkedin.com/company/<短名> 里的短名（如 microsoft），也可以传完整链接；不认工商注册名。
- `job` 传 `jobs` 结果里的 `url`，形如 https://www.linkedin.com/jobs/view/<数字>/。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"linkedin","action":"search","params":{"keyword":"data engineering"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`company_profile`、`company_posts`、`jobs`、`job_detail` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $3.19 |
| 公司主页 | `company_profile` | $0.56 |
| 公司动态 | `company_posts` | $2.32 |
| 职位搜索 | `jobs` | $0.56 |
| 职位详情 | `job_detail` | $1.19 |

- 按调用次数计费，每次约 $0.00056 到 $0.0032；失败、空结果、参数错误和鉴权失败都不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>
- LinkedIn 其他 7 个能力的单价见平台页 <https://everyinfra.com/linkedin-api?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

### 返回字段

下面是这 5 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_username` | 作者用户名（@handle），通常可用于拼 URL。 |
| `author_headline` | 内容作者的 headline（帖子/评论里用）。 |
| `author_url` | 作者在原平台的主页链接。 |
| `author_avatar_url` | 帖子作者头像链接（search、post_detail）。 |
| `author_type` | 帖子作者类型：profile（个人）/ company（公司）。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `share_count` | 帖子被转发的次数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `reactions` | 各类反应数（search）：每项 type（like、appreciation、empathy 等）与 count。 |

完整参数和字段：<https://everyinfra.com/linkedin-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

#### `company_profile`（公司主页）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `name` | 名称。 |
| `universal_name` | 公司在 LinkedIn 的 URL 短名。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `description` | 简介或描述，通常比 text 短。 |
| `website` | 账号或商家填写的外链网址。 |
| `industries` | 所属行业。 |
| `specialties` | 公司专长领域。 |
| `employee_count` | 员工数。 |
| `employee_count_range` | LinkedIn 官方展示的员工数区间（如 10001+），比 employee_count 更稳定。 |
| `follower_count` | 粉丝数。 |
| `is_verified` | 是否为平台认证账号（蓝V等）。 |
| `headquarters` | 总部所在地。 |
| `logo_url` | logo 链接。 |
| `cover_url` | 公司主页背景大图链接。 |
| `hashtags` | 公司/帖子的话题标签列表。 |
| `job_search_url` | 该公司在 LinkedIn 的招聘搜索链接。 |
| `offices` | 办公地点列表：每项含城市、州/省、国家、街道地址、是否总部与所在大区 region。 |
| `headquarters_postal_code` | 总部邮编。 |
| `latitude` | 总部纬度。 |
| `longitude` | 总部经度。 |
| `page_type` | 页面类型：COMPANY（公司）/ SCHOOL（学校）/ SHOWCASE（展示页）。 |
| `call_to_action` | 公司页的行动按钮：text（如 Visit website）、url、type。 |
| `similar_company_ids` | LinkedIn 推荐的相似公司（数字 ID，可再用 company_profile 查）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/linkedin-api/company_profile?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

#### `company_posts`（公司动态）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `author_name` | 作者昵称（显示名）。 |
| `author_username` | 作者用户名（@handle），通常可用于拼 URL。 |
| `author_headline` | 内容作者的 headline（帖子/评论里用）。 |
| `author_url` | 作者在原平台的主页链接。 |
| `author_avatar_url` | 帖子作者头像链接（search、post_detail）。 |
| `author_type` | 帖子作者类型：profile（个人）/ company（公司）。 |
| `reactions` | 各类反应数（search）：每项 type（like、appreciation、empathy 等）与 count。 |
| `like_count` | 点赞数。 |
| `comment_count` | 评论数。 |
| `share_count` | 帖子被转发的次数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `author_id` | 帖子作者的数字成员 ID（search）。 |
| `attachment` | 帖子附带的卡片（search）：type（如 job、article）、title、description、subtitle、url、image_url。 |
| `is_reshare` | 帖子是否为转发。 |

完整参数和字段：<https://everyinfra.com/linkedin-api/company_posts?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

#### `jobs`（职位搜索）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `title` | 标题。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `company_name` | 公司名称。 |
| `company_url` | 公司主页链接。 |
| `company_logo` | 公司 logo。 |
| `location` | 地理位置描述，原文透传，格式随平台而异。 |
| `salary` | 薪酬信息。 |
| `employment_type` | 雇佣类型（全职/兼职/合同/实习）。 |
| `seniority` | 职级。 |
| `applicant_count` | 岗位已投递人数。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/linkedin-api/jobs?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

#### `job_detail`（职位详情）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `title` | 标题。 |
| `text` | 正文内容，已去除 HTML 标签，全文返回、不截断（个别平台的列表结果本身只有摘要，以该平台的字段说明为准）。 |
| `company_name` | 公司名称。 |
| `company_url` | 公司主页链接。 |
| `company_logo` | 公司 logo。 |
| `location` | 地理位置描述，原文透传，格式随平台而异。 |
| `employment_type` | 雇佣类型（全职/兼职/合同/实习）。 |
| `posted_at` | 发布时间，ISO 8601 格式、UTC 时区（如 2026-08-07T12:34:56+00:00）。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `apply_url` | 投递链接（job_detail）：站外投递页或 LinkedIn 一键投递链接。 |
| `workplace_type` | 办公方式（job_detail）：onsite 现场 / remote 远程 / hybrid 混合。 |
| `is_remote` | 是否可远程（job_detail）。 |
| `industries` | 所属行业。 |
| `salary` | 薪酬信息。 |
| `applicant_count` | 岗位已投递人数。 |
| `benefits` | 职位页列出的福利（job_detail），没有时没有这个字段。 |
| `view_count` | 浏览/播放数。 |
| `job_state` | 职位状态（job_detail）：LISTED 在招 / CLOSED 已关闭。 |
| `country_code` | 国家代码。 |
| `expires_at` | 职位到期时间（job_detail），ISO 8601 UTC。 |
| `company_employee_count` | 招聘公司的员工数（job_detail，LinkedIn 公司页口径）。 |
| `company_website` | 招聘公司官网（job_detail）。 |

完整参数和字段：<https://everyinfra.com/linkedin-api/job_detail?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

### 常见问题

**调用时要不要提供 LinkedIn 账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $0.56 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

**能把 LinkedIn 接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>。

**用 LinkedIn 数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到 LinkedIn 的哪些数据？**

LinkedIn 有 12 个能力：关键词搜索、账号搜索、个人职业资料、公司主页、评论、粉丝数量、职位搜索、员工列表、公司动态、个人动态、职位详情、内容详情。每个能力的参数和返回字段见平台页 <https://everyinfra.com/linkedin-api?utm_source=github&utm_medium=example_repo&utm_campaign=linkedin-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 5 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search "data engineering" --out posts.csv` | 2026-11-25 12:15 | 10 | $0.003194 |
| `python main.py company microsoft --out company.json` | 2026-11-25 12:16 | 1 | $0.000556 |
| `python main.py company-posts microsoft --out company_posts.csv` | 2026-11-25 12:16 | 10 | $0.002319 |
| `python main.py jobs "data engineer" --out jobs.csv` | 2026-11-25 12:16 | 20 | $0.000556 |
| `python main.py job "<职位链接>" --out job.json` | 2026-11-25 12:17 | 1 | $0.001194 |

`company_profile` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "id": "1035",
  "description": "Every company has a mission. What's ours? To empower every p…",
  "employee_count": 230402,
  "follower_count": 29587063
}
```

## License

MIT
