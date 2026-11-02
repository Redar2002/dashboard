import os
import sys
import types

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

# pyodbc a besoin de la bibliothèque système ODBC : on la remplace par un faux module si elle manque.
try:
    import pyodbc  # noqa: F401
except ImportError:
    fake = types.ModuleType("pyodbc")
    fake.drivers = lambda: []

    def _connect(*args, **kwargs):
        raise RuntimeError("pyodbc indisponible dans les tests")

    fake.connect = _connect
    sys.modules["pyodbc"] = fake
