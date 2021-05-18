import os
import sys

if hasattr(sys, 'frozen'):
    main_dir = os.path.dirname(sys.executable)
else:
    main_dir = os.path.split(sys.argv[0])[0]
