"""Verification script to check if the multi-agent system is ready to use."""
import sys
import os

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (requires 3.8+)")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    print("\nChecking dependencies...")
    required_packages = [
        'streamlit',
        'langchain',
        'langchain_openai',
        'langchain_community',
        'langchain_core',
        'dotenv'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (not installed)")
            all_installed = False
    
    return all_installed

def check_agents():
    """Check if agent modules can be imported."""
    print("\nChecking agent modules...")
    try:
        from agents import MathAgent, SQLAgent, SearchAgent, SupervisorAgent
        print("✅ All agent modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Error importing agents: {e}")
        return False

def check_env_file():
    """Check if .env file exists."""
    print("\nChecking environment configuration...")
    if os.path.exists('.env'):
        print("✅ .env file exists")
        return True
    else:
        print("⚠️  .env file not found (copy from .env.example)")
        return False

def check_api_keys():
    """Check if API keys are configured."""
    print("\nChecking API keys...")
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    serpapi_key = os.getenv('SERPAPI_API_KEY')
    
    results = []
    
    if openai_key:
        print("✅ OPENAI_API_KEY is set")
        results.append(True)
    else:
        print("❌ OPENAI_API_KEY is not set (required)")
        results.append(False)
    
    if serpapi_key:
        print("✅ SERPAPI_API_KEY is set")
    else:
        print("ℹ️  SERPAPI_API_KEY not set (optional - search will use LLM knowledge)")
    
    return all(results)

def check_files():
    """Check if all necessary files exist."""
    print("\nChecking project files...")
    required_files = [
        'app.py',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'README.md',
        'agents/__init__.py',
        'agents/math_agent.py',
        'agents/sql_agent.py',
        'agents/search_agent.py',
        'agents/supervisor_agent.py'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (missing)")
            all_exist = False
    
    return all_exist

def main():
    """Run all verification checks."""
    print("=" * 70)
    print("Multi-Agent System Installation Verification")
    print("=" * 70)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Agent Modules", check_agents),
        ("Project Files", check_files),
        ("Environment File", check_env_file),
        ("API Keys", check_api_keys),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Error during {check_name}: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 70)
    print("Verification Summary")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total} checks")
    
    if all(results):
        print("\n✅ All checks passed! You're ready to use the multi-agent system.")
        print("\nNext steps:")
        print("  1. Run the application: streamlit run app.py")
        print("  2. Or try the demo: python demo.py")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        print("\nCommon solutions:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Create .env file: cp .env.example .env")
        print("  3. Add your OPENAI_API_KEY to .env file")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
