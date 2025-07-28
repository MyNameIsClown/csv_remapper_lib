import json
import time
from datetime import datetime, timedelta
from csv_remapper_lib import CSVFile, MergeType, ConnectorType

import pytest


def test_all_operations_timing():
    data_path = "tests/data/huge_sample.csv"
    new_data_path = "tests/data/huge_sample_transformed.csv"

    operations = {}

    csv = CSVFile(data_path)

    # Convertir a número positivo
    start = time.perf_counter()
    
    csv.to_positive_number('NegativeNum')
    operations['to_positive_number'] = time.perf_counter() - start

    # Convertir a número negativo
    start = time.perf_counter()
    
    csv.to_negative_number('PositiveNum')
    operations['to_negative_number'] = time.perf_counter() - start

    # Convertir a fecha ISO
    start = time.perf_counter()
    
    csv.to_date('DateString')
    operations['to_date'] = time.perf_counter() - start

    # Renombrar múltiples claves
    start = time.perf_counter()
    csv.rename_keys({'ID':'Identifier','FirstName':'FName','LastName':'LName'})
    operations['rename_keys'] = time.perf_counter() - start

    # Renombrar una clave
    start = time.perf_counter()
    csv.rename_key('Num1','Number1')
    operations['rename_key'] = time.perf_counter() - start

    # Eliminar múltiples claves
    start = time.perf_counter()
    csv.remove_keys(['PositiveNum','NegativeNum'])
    operations['remove_keys'] = time.perf_counter() - start

    # Eliminar una clave
    start = time.perf_counter()
    csv.remove_key('Identifier')
    operations['remove_key'] = time.perf_counter() - start

    # Merge TEXT
    start = time.perf_counter()
    
    connector = ConnectorType(MergeType.TEXT, delimiter=' ')
    csv.merge_keys(['FName','LName'], connector, 'FullName', delete_old_keys=True)
    operations['merge_text'] = time.perf_counter() - start

    # Merge NUMBER
    start = time.perf_counter()
    
    connector = ConnectorType(MergeType.NUMBER, operator='+')
    csv.merge_keys(['Number1','Num2'], connector, 'NumSum', delete_old_keys=True)
    operations['merge_number'] = time.perf_counter() - start

    # Merge PERCENTAGE
    start = time.perf_counter()
    
    connector = ConnectorType(MergeType.PERCENTAGE)
    csv.merge_keys(['BaseValue','ValueForPct'], connector, 'PctValue', delete_old_keys=True)
    operations['merge_percentage'] = time.perf_counter() - start

    # Merge DATE
    start = time.perf_counter()
    
    connector = ConnectorType(MergeType.DATE, operator='-', time_format='d')
    csv.merge_keys(['Date1','Date2'], connector, 'DaysDiff', delete_old_keys=True)
    operations['merge_date'] = time.perf_counter() - start

    # Merge TIME
    start = time.perf_counter()
    
    connector = ConnectorType(MergeType.TIME, operator='+')
    csv.merge_keys(['Time1','Time2'], connector, 'TimeSum', delete_old_keys=True)
    operations['merge_time'] = time.perf_counter() - start

    # SAVE
    start = time.perf_counter()
    csv.save(new_data_path)
    operations['saving'] = time.perf_counter() - start

    # Total
    total = sum(operations.values())
    operations['TOTAL'] = total

    # Guardar tiempos en JSON
    with open('tests/data/timing_execution.json','w') as f:
        json.dump(operations, f, indent=4)

    assert 'TOTAL' in operations
