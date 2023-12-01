import cx_Freeze

executables = [cx_Freeze.Executable('peguealinguagem.py')]

cx_Freeze.setup(
    name="Pegue a Linguagem",
    options={'build_exe': {'packages':['pygame'],
                           'include_files':['images']}},

    executables = executables
    
)