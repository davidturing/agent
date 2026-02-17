import subprocess
import os
import datetime

REPO_PATH = "/Users/zhaoqinhuang/david_project"
KNOWLEDGE_PATH = "skills/self-learning-agent/pageindex/knowledge"

def push_to_github():
    """Commit and push new knowledge to the GitHub repository."""
    print("\n[Stage 5] Syncing Knowledge to GitHub")
    
    try:
        # Check if there are changes in the knowledge directory
        status = subprocess.run(
            ["git", "status", "--short", KNOWLEDGE_PATH],
            capture_output=True, text=True, cwd=REPO_PATH
        )
        
        if not status.stdout.strip():
            print("No new knowledge to sync.")
            return

        # Add only the knowledge directory
        subprocess.run(["git", "add", KNOWLEDGE_PATH], cwd=REPO_PATH, check=True)
        
        # Commit with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"David Agent: Update Knowledge Graph - {timestamp}"
        subprocess.run(["git", "commit", "-m", commit_message], cwd=REPO_PATH, check=True)
        
        # Push to the target knowledge repository (davidturing/agent)
        # Using the subtree strategy to only push the knowledge directory
        # Format: git subtree push --prefix=DIR REMOTE BRANCH
        print(f"Syncing knowledge to davidturing/agent...")
        result = subprocess.run(
            ["git", "subtree", "push", "--prefix", KNOWLEDGE_PATH, "knowledge", "main"],
            capture_output=True, text=True, cwd=REPO_PATH
        )
        
        if result.returncode == 0:
            print(f"Successfully pushed knowledge to davidturing/agent.")
        else:
            # Fallback to normal push if subtree fails (e.g. repo initialization)
            print(f"Subtree push failed, attempting standard push to 'knowledge' remote...")
            result = subprocess.run(["git", "push", "knowledge", "main"], capture_output=True, text=True, cwd=REPO_PATH)
            
        if result.returncode == 0:
            print("Sync complete.")
        else:
            print(f"Git push failed: {result.stderr}")
            
    except Exception as e:
        print(f"GitHub Sync failed: {e}")

if __name__ == "__main__":
    push_to_github()
