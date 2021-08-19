__version__ = '0.1.0'

import platform, subprocess, tempfile, os, shutil

def get_platform():
    """Returna a string identifying the current platform.

    Returns:
        str: A string identifying the current platform.
    """
    return platform.system()

def is_windows():
    """Returns true if the current platform is Windows.

    Returns:
        bool: A boolean indicating if the current platform is Windows.
    """
    return get_platform().upper() == 'Windows'.upper()

def is_linux():
    """Returns true if the current platform is Linux.

    Returns:
        bool: A boolean indicating if the current platform is Linux.
    """
    return get_platform().upper() == 'Linux'.upper()

def is_osx():
    """Returns true if the current platform is OSX (MacOS).

    Returns:
        bool: A boolean indicating if the current platform is OSX (MacOS).
    """
    return get_platform().upper() == 'Darwin'.upper()

def get_office_cli_path():
    """Returns the path to the LibreOffice command line interface.

    Returns:
        str: The path to the command line interface.
    """
    if is_windows():
        raise NotImplementedError('Windows is not supported.')
    elif is_linux():
        if not os.path.exists('/usr/bin/soffice'):
            raise Exception(f'Could not find LibreOffice. Is it installed?')
        return '/usr/bin/soffice'
    elif is_osx():
        if not os.path.exists('/Applications/LibreOffice.app/Contents/MacOS/soffice'):
            raise Exception(f'Could not find LibreOffice.app. Is it installed?')
        return '/Applications/LibreOffice.app/Contents/MacOS/soffice'
    else:
        raise Exception('Unsupported platform')
    
def convert(in_file, out_file=None):
    """Converts a file to PDF.

    Args:
        in_file (str): The path to the input file.
        out_file (str): The path to the output file, same path to in_file if not passes.
    """
    
    if not out_file:
        outdir = os.path.dirname(in_file)
    else:
        outdir = tempfile.gettempdir()
    
    command_line = get_office_cli_path()
    subprocess.call([
        command_line, 
        '--headless',
        '--convert-to',
        'pdf',
        '--outdir', 
        outdir,
        in_file
    ])
    
    if out_file:
        out_temp_file_arr = os.path.splitext(in_file)
        out_temp_file_name =  f'{os.path.basename(out_temp_file_arr[0])}.pdf'
        out_file = f'{os.path.splitext(out_file)[0]}.pdf'
        shutil.move(os.path.join(outdir, out_temp_file_name), out_file)
        