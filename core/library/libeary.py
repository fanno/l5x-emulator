import os
import shutil
import sys
import glob
import yaml
import logging

def get_project_root():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        if sys.argv and os.path.isfile(sys.argv[0]):
            entry_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

            if os.path.isdir(os.path.join(entry_dir, 'library')):
                return entry_dir
        
        cwd = os.getcwd()
        if os.path.isdir(os.path.join(cwd, 'library')):
            return cwd
            
        return os.path.dirname(os.path.abspath(__file__))

def get_paths():
    root = get_project_root()
    
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        
        return {
            'base': root,
            'exe': exe_dir,
            'library': os.path.join(root, 'library', 'hardware'),
            'templates': os.path.join(root, 'templates', 'hardware'),
            'custom': os.path.join(exe_dir, 'custom', 'hardware')
        }
    else:
        return {
            'base': root,
            'exe': root,
            'library': os.path.join(root, 'library', 'hardware'),
            'templates': os.path.join(root, 'templates', 'hardware'),
            'custom': os.path.join(root, 'custom', 'hardware')
        }
    
def isPyInstaller():
    return getattr(sys, 'frozen', False)

def initPyInstaller():
    if isPyInstaller():
        path = get_paths()        

        files:list[list[str]] = []

        base_dir = path['base']
        exe_dir = path['exe']

        files.append([os.path.join(base_dir, 'templates', 'hardware'), os.path.join(exe_dir, 'custom', 'hardware')])

        files.append([os.path.join(base_dir, 'Plc_emulator.L5X'), os.path.join(exe_dir)])
        files.append([os.path.join(base_dir, 'errorcodes.json'), os.path.join(exe_dir)])

        for file in files:
            s, d  = file
            copy(s, d)

def copy(src, dest):
    if isPyInstaller():
        if not os.path.exists(dest):
            os.makedirs(dest, exist_ok=True)
            logging.debug(f"Created: {dest}")

        if not os.path.exists(src):
            logging.debug(f"ERROR: Source not found at {src}")
            input("Press Enter to exit...")
            #TODO THORW EXCEPTION
            return

        try:
            if os.path.isfile(src):
                shutil.copy2(src, dest)
            else:
                shutil.copytree(src, dest, dirs_exist_ok=True)
        except Exception as e:
            logging.exception(e)
            #TODO THORW EXCEPTION
            input("Press Enter to exit...")


def load_all_hardware(paths):
    registry = {}
    
    def load_yaml_file(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data and isinstance(data, dict):
                    dev_id = data.get('id') or data.get('name')
                    if dev_id:
                        return dev_id, data
        except Exception as e:
            logging.exception(f"[Load] Error parsing {filepath}: {e}")
        return None, None

    lib_path = paths['library']
    if os.path.exists(lib_path):
        logging.debug(f"[Load] Scanning Library: {lib_path}")
        for filepath in glob.glob(os.path.join(lib_path, "*.yaml")):
            dev_id, data = load_yaml_file(filepath)
            if dev_id:
                registry[dev_id] = {
                    'source': 'library',
                    'data': data
                }
    else:
        ## THROW EXCEPTION
        logging.debug(f"[Load] Library folder not found: {lib_path}")

    cust_path = paths['custom']
    if os.path.exists(cust_path):
        logging.debug(f"[Load] Scanning Custom: {cust_path}")
        for filepath in glob.glob(os.path.join(cust_path, "*.yaml")):
            dev_id, data = load_yaml_file(filepath)
            if dev_id:
                # OVERWRITE logic: Custom takes precedence
                if dev_id in registry:
                    logging.debug(f"[Load] Override: '{dev_id}' loaded from Custom (replacing Library).")
                
                registry[dev_id] = {
                    'source': 'custom',
                    'data': data
                }

    return registry