#!/usr/bin/env python
"""
Development environment setup script
Decision: Automate common setup tasks for new developers
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run shell command with error handling"""
    print(f"→ {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"  {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Error: {e.stderr.strip()}")
        return False

def main():
    """Set up development environment"""
    print("🚀 Setting up VLE User Management System for development\n")
    
    # Check if we're in the right directory
    if not Path('src/manage.py').exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if .env exists
    if not Path('.env').exists():
        print("📝 Creating .env file from template")
        try:
            with open('.env.example', 'r') as source:
                content = source.read()
            with open('.env', 'w') as dest:
                dest.write(content)
            print("✅ Created .env file - please update it with your settings")
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            sys.exit(1)
    
    # Install dependencies
    print("\n📦 Installing Python dependencies")
    if not run_command("pip install -r requirements/development.txt", "Installing packages"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Run migrations
    print("\n🗄️  Setting up database")
    os.chdir('src')
    
    if not run_command("python manage.py migrate", "Running database migrations"):
        print("❌ Database migration failed")
        sys.exit(1)
    
    # Create superuser (optional)
    print("\n👤 Create superuser account (optional - press Ctrl+C to skip)")
    try:
        subprocess.run("python manage.py createsuperuser", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n  Skipped superuser creation")
    except subprocess.CalledProcessError:
        print("  Superuser creation failed or was cancelled")
    
    # Run tests
    print("\n🧪 Running tests to verify setup")
    if run_command("python manage.py test", "Running test suite"):
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed - check configuration")
    
    print(f"""
🎉 Development setup complete!

Next steps:
1. Update .env file with your database credentials
2. Start the development server:
   cd src
   python manage.py runserver

3. Visit: http://127.0.0.1:8000/admin/ (if you created a superuser)
4. API docs: http://127.0.0.1:8000/api/v1/

Feature flags in .env:
- Set ENABLE_* variables to True/False per client needs
""")

if __name__ == '__main__':
    main()