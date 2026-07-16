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
            'base': root,          # Points to _internal
            'exe': exe_dir,        # Points to dist/plc
            'library': os.path.join(root, 'library', 'hardware'),
            'templates': os.path.join(root, 'templates', 'hardware'),
            'custom': os.path.join(exe_dir, 'custom', 'hardware')
        }
    else:
        return {
            'base': root,
            'exe': root,           # In dev, we write to the project root
            'library': os.path.join(root, 'library', 'hardware'),
            'templates': os.path.join(root, 'templates', 'hardware'), # Note: 'custom' source is here
            'custom': os.path.join(root, 'custom', 'hardware')
        }

def initialize_custom_folder():
    if getattr(sys, 'frozen', False):
        path = get_paths()        

        base_dir = path['base']
        exe_dir = path['exe']

        template_src_dir = os.path.join(base_dir, 'templates', 'hardware')
        
        user_dest_dir = os.path.join(exe_dir, 'custom', 'hardware')

        if not os.path.exists(user_dest_dir):
            os.makedirs(user_dest_dir, exist_ok=True)
            logging.debug(f"Created: {user_dest_dir}")

        if not os.path.exists(template_src_dir):
            logging.debug(f"ERROR: Source not found at {template_src_dir}")
            input("Press Enter to exit...")
            #TODO THORW EXCEPTION
            return

        try:
            files = os.listdir(template_src_dir)
            
            for filename in files:
                src_file = os.path.join(template_src_dir, filename)
                dst_file = os.path.join(user_dest_dir, filename)

                if os.path.isdir(src_file):
                    continue

                if not os.path.exists(dst_file):
                    shutil.copy2(src_file, dst_file)
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