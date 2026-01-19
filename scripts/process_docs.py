import os, re, requests, sys

def main():
    token = os.getenv('CLICKUP_TOKEN')
    repo_full = os.getenv('GITHUB_REPOSITORY')
    sha = os.getenv('GITHUB_SHA')[:7]
    
    # 1. Read the developer's requirements
    try:
        with open('docs/requirements.md', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: docs/requirements.md not found")
        return
    
    # 2. Extract IDs using Regex
    # Matches internal ID: DIG-F/2025/26
    internal_id_match = re.search(r'ID:\s*(DIG-F/[\d/]+)', content)
    # Matches ClickUp Task ID: 8678zb4qy (usually 7-10 characters)
    clickup_id_match = re.search(r'ClickUp:\s*(\w+)', content)
    
    if not clickup_id_match: 
        print("No ClickUp Task ID found in file. Use 'ClickUp: <id>'")
        return
    
    task_id = clickup_id_match.group(1)
    internal_id = internal_id_match.group(1) if internal_id_match else "Unknown"

    # 3. Construct the URL for the Documentation Portal
    user, repo = repo_full.split('/')
    portal_url = f"https://{user}.github.io/Company-Docs-Portal/features/{sha}/"
    
    # 4. Post the link to ClickUp
    url = f"https://api.clickup.com/api/v2/task/{task_id}/comment"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    payload = {
        "comment_text": f"📄 **Spec Generated for {internal_id}**\n🔗 View documentation: {portal_url}"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    print(f"ClickUp Response: {response.status_code}")

if __name__ == "__main__":
    main()