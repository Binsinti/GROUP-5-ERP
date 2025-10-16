import os
import shutil

def clear_pycache(directory):
    """Recursively delete all __pycache__ directories and .pyc files"""
    deleted_dirs = 0
    deleted_files = 0
    
    for root, dirs, files in os.walk(directory):
        # Delete .pyc files
        for file in files:
            if file.endswith('.pyc'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    deleted_files += 1
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        
        # Delete __pycache__ directories
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(pycache_path)
                deleted_dirs += 1
                print(f"Deleted directory: {pycache_path}")
            except Exception as e:
                print(f"Error deleting {pycache_path}: {e}")
    
    print(f"\n✓ Cleared {deleted_files} .pyc files and {deleted_dirs} __pycache__ directories")

if __name__ == '__main__':
    project_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Clearing Python cache in: {project_dir}")
    clear_pycache(project_dir)
    print("\n✓ Cache cleared successfully!")

