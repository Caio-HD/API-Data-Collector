"""
Unit tests for exporters
"""

import pytest
import json
import csv
from pathlib import Path
from src.exporters.json_exporter import JSONExporter
from src.exporters.csv_exporter import CSVExporter


class TestJSONExporter:
    """Test cases for JSONExporter."""
    
    def test_init(self, temp_output_dir):
        """Test exporter initialization."""
        exporter = JSONExporter(output_dir=temp_output_dir)
        assert exporter.output_dir == Path(temp_output_dir)
        assert exporter.indent == 2
    
    def test_export_single_dict(self, temp_output_dir):
        """Test exporting a single dictionary."""
        exporter = JSONExporter(output_dir=temp_output_dir)
        data = {"name": "test", "value": 123}
        
        file_path = exporter.export(data, "test.json")
        
        assert Path(file_path).exists()
        with open(file_path, 'r') as f:
            loaded = json.load(f)
            assert loaded == data
    
    def test_export_list(self, temp_output_dir):
        """Test exporting a list."""
        exporter = JSONExporter(output_dir=temp_output_dir)
        data = [{"id": 1}, {"id": 2}]
        
        file_path = exporter.export(data, "test_list.json")
        
        assert Path(file_path).exists()
        with open(file_path, 'r') as f:
            loaded = json.load(f)
            assert len(loaded) == 2
    
    def test_export_auto_extension(self, temp_output_dir):
        """Test automatic .json extension addition."""
        exporter = JSONExporter(output_dir=temp_output_dir)
        data = {"test": "data"}
        
        file_path = exporter.export(data, "test")
        
        assert file_path.endswith('.json')
        assert Path(file_path).exists()
    
    def test_export_multiple(self, temp_output_dir):
        """Test exporting multiple datasets."""
        exporter = JSONExporter(output_dir=temp_output_dir)
        data_dict = {
            "repos": [{"id": 1}],
            "issues": [{"id": 2}]
        }
        
        files = exporter.export_multiple(data_dict, prefix="test_")
        
        assert len(files) == 2
        assert all(Path(f).exists() for f in files)


class TestCSVExporter:
    """Test cases for CSVExporter."""
    
    def test_init(self, temp_output_dir):
        """Test exporter initialization."""
        exporter = CSVExporter(output_dir=temp_output_dir)
        assert exporter.output_dir == Path(temp_output_dir)
    
    def test_export_list_of_dicts(self, temp_output_dir):
        """Test exporting list of dictionaries."""
        exporter = CSVExporter(output_dir=temp_output_dir)
        data = [
            {"name": "Item 1", "value": 10},
            {"name": "Item 2", "value": 20}
        ]
        
        file_path = exporter.export(data, "test.csv")
        
        assert Path(file_path).exists()
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 2
            assert rows[0]['name'] == 'Item 1'
    
    def test_export_single_dict(self, temp_output_dir):
        """Test exporting single dictionary."""
        exporter = CSVExporter(output_dir=temp_output_dir)
        data = {"name": "Item", "value": 10}
        
        file_path = exporter.export(data, "test_single.csv")
        
        assert Path(file_path).exists()
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 1
    
    def test_export_auto_extension(self, temp_output_dir):
        """Test automatic .csv extension addition."""
        exporter = CSVExporter(output_dir=temp_output_dir)
        data = [{"test": "data"}]
        
        file_path = exporter.export(data, "test")
        
        assert file_path.endswith('.csv')
        assert Path(file_path).exists()
    
    def test_flatten_nested_dict(self, temp_output_dir):
        """Test flattening nested dictionaries."""
        exporter = CSVExporter(output_dir=temp_output_dir)
        data = [
            {
                "name": "Item",
                "nested": {
                    "value": 10,
                    "other": "test"
                }
            }
        ]
        
        file_path = exporter.export(data, "test_nested.csv", flatten_nested=True)
        
        assert Path(file_path).exists()
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert 'nested_value' in rows[0]
            assert 'nested_other' in rows[0]
    
    def test_format_value(self, temp_output_dir):
        """Test value formatting."""
        exporter = CSVExporter(output_dir=temp_output_dir)
        
        assert exporter._format_value(None) == ''
        assert exporter._format_value(True) == 'true'
        assert exporter._format_value(False) == 'false'
        assert exporter._format_value(123) == '123'
