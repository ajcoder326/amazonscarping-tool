"""
Build script to create exe using PyInstaller
Run: python build_exe.py
"""
import subprocess
import sys
import os
from pathlib import Path
import io

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def build_exe():
    """Build executable using PyInstaller"""
    
    # Get project directory
    project_dir = Path(__file__).parent
    
    print("🔨 Building Amazon Traffic Simulator EXE...")
    print(f"Project directory: {project_dir}")
    
    # Find playwright stealth module path
    import playwright_stealth
    stealth_path = Path(playwright_stealth.__file__).parent
    
    # PyInstaller command
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=Amazon_Traffic_Simulator",
        "--onefile",  # Single exe file
        "--windowed",  # No console window
        "--icon=NONE",  # No icon (can add later)
        "--add-data", "run_with_cookies.py:.",
        "--add-data", "traffic_simulator.py:.",
        "--add-data", "amazon_cookies.json:.",
        "--add-data", "run_traffic.py:.",
        "--add-data", f"{stealth_path}:playwright_stealth",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=playwright",
        "--hidden-import=playwright_stealth",
        str(project_dir / "gui_app.py")
    ]
    
    print("\n📝 PyInstaller Command:")
    print(" ".join(cmd))
    print("\n⏳ Building... This may take a few minutes...\n")
    
    try:
        result = subprocess.run(cmd, cwd=str(project_dir), check=True)
        
        exe_path = project_dir / "dist" / "Amazon_Traffic_Simulator.exe"
        
        if exe_path.exists():
            print(f"\n✅ Build successful!")
            print(f"📁 EXE Location: {exe_path}")
            print(f"📦 File Size: {exe_path.stat().st_size / (1024*1024):.1f} MB")
            return True
        else:
            print(f"\n❌ Build completed but exe not found at {exe_path}")
            return False
    
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Build error: {str(e)}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
