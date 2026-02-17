
import sys
import os
from dotenv import load_dotenv

# Add src directory to sys.path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import doctor
    import ingest
    import ingest_x
    import brain
    import brain_graph
    import publish
    import release_github
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def main():
    print("--- 🚀 David Agent Pipeline (Flat Mode) ---")
    
    # 1. Doctor
    print("\n[Stage 1] Doctor Check")
    try:
        if not doctor.generate_report():
            print("❌ Health Check Failed. Aborting.")
            return
    except Exception as e:
        print(f"Doctor failed: {e}")
        return

    # 2. Ingest
    print("\n[Stage 2] Ingestion")
    try:
        ingest.fetch_github_events()
        ingest.fetch_self_code()
        # ingest_x.fetch_x_tweets() # Temporarily disabled due to auth/timeout issues
    except Exception as e:
        print(f"Ingestion failed: {e}")

    # 3. Brain
    print("\n[Stage 3] Brain Processing")
    try:
        brain.main()
        brain_graph.process_latest_x_data()
    except Exception as e:
        print(f"Brain failed: {e}")

    # 4. Publish
    print("\n[Stage 4] Publication")
    try:
        publish.main()
        release_github.push_to_github()
    except Exception as e:
        print(f"Publish failed: {e}")

    print("\n--- ✅ Pipeline Completed ---")

if __name__ == "__main__":
    main()
