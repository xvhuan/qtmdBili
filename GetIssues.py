import requests


# 函数用于验证GitHub令牌的有效性
def validate_github_token(token):
    headers = {"Authorization": f"token {token}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    return response.status_code == 200


# 函数用于从GitHub获取指定状态的问题列表
def get_github_issues(owner, repo, token, state, page):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {"Authorization": f"token {token}"}
    params = {"state": state, "page": page, "per_page": 100}  # 每页最多获取100个问题
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch issues: {response.status_code}")
        return None


# 函数用于获取用户输入的GitHub仓库信息
def get_repo_info():
    while True:
        repo_url = input("请输入 GitHub 仓库网址（例如 https://github.com/owner_name/repo_name）: ")
        parts = repo_url.strip("/").split("/")
        if len(parts) == 5 and parts[0] == "https:" and parts[2] == "github.com":
            owner = parts[3]
            repo = parts[4]
            return owner, repo
        else:
            print("请输入有效的 GitHub 仓库网址！")


# 函数用于获取指定状态下的问题的最大页数
def get_max_page(owner, repo, token, state):
    page = 1
    while True:
        issues = get_github_issues(owner, repo, token, state, page)
        if issues:
            page += 1
        else:
            break
    return page - 1


# 主程序逻辑
def main():
    # 获取用户输入的GitHub仓库信息
    owner, repo = get_repo_info()

    # 获取要查询的问题状态
    while True:
        state = input("请输入要查询的问题状态（'open(o)' 或 'closed(c)'）: ")
        state = state.lower()
        if state in ['open', 'closed']:
            break
        elif state == "o":
            state = 'open'
            break
        elif state == "c":
            state = 'closed'
            break
        else:
            print("请输入有效的状态！")

    # 获取指定状态下的问题的最大页数
    max_page = get_max_page(owner, repo, token, state)

    # 获取用户输入的要查询的页数
    while True:
        page = input(f"请输入要查询的页数（0为最新的一页，最大页数为{max_page}）: ")
        if page.isdigit() and 0 <= int(page) <= max_page:
            page = int(page)
            break
        else:
            print(f"请输入有效的页数！")

    # 获取指定状态下指定页数的问题列表并显示
    issues = get_github_issues(owner, repo, token, state, page)
    if issues:
        print(f"Issues for {owner}/{repo}, State: {state.capitalize()}, Page {page}:")
        for issue in issues:
            print(f"Title: {issue['title']}")
            print("Body:")
            print(issue['body'])
            print("-" * 50)
        print(f"总共找到 {len(issues)} 个问题。")


if __name__ == "__main__":
    # 用户输入GitHub令牌并验证其有效性
    token = input("请输入您的GitHub令牌：")
    while not token.startswith("ghp") or not validate_github_token(token):
        print("警告：令牌格式不正确或令牌无效，请重新输入")
        token = input("在这里填写:")

    # 执行主程序逻辑
    main()
