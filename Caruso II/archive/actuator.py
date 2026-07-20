import sys
from pathlib import Path
import clr

class DotNetActuator:
    def __init__(self, sdk_directory: str):
        sdk_directory = Path(sdk_directory).resolve()

        if not sdk_directory.exists():
            raise FileNotFoundError(sdk_directory)

        sys.path.append(str(sdk_directory))

        # path to the dynamic link library (.dll)
        clr.AddReference(r"C:\Program Files\Thorlabs XA\SDK\.NET Framework (C#)\Libraries\x64\tlmc_xa_dotnet")

        # Replace these with the actual namespace and class names.
        from DotNet_Windows_DLL_Examples.Program import Controller

        # self._controller = Controller()
        # self._connected = False

    