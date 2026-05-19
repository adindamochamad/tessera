"""
Tests untuk Query Analyzer

Testing berbagai scenarios untuk detection violation patterns.
"""

import pytest
from app.analyzers.query_analyzer import MongoDBQueryAnalyzer, QueryAnalysisResult


@pytest.fixture
def analyzer():
    """Fixture untuk analyzer instance."""
    return MongoDBQueryAnalyzer()


def test_detect_missing_tenant_filter(analyzer):
    """Test detection query tanpa tenant filter."""
    query = {
        "collection": "orders",
        "command": "find",
        "filter": {
            "status": "pending"
        }
    }
    
    result = analyzer.analyze(query)
    
    assert result.koleksi == "orders"
    assert result.ada_tenant_filter is False
    assert "missing_tenant_filter" in result.pattern_violations


def test_safe_query_with_tenant_filter(analyzer):
    """Test query yang aman dengan tenant filter."""
    query = {
        "collection": "orders",
        "command": "find",
        "filter": {
            "tenant_id": "acme-corp",
            "status": "pending"
        }
    }
    
    result = analyzer.analyze(query)
    
    assert result.koleksi == "orders"
    assert result.ada_tenant_filter is True
    assert result.field_tenant == "tenant_id"
    assert len(result.pattern_violations) == 0


def test_detect_cross_tenant_aggregation(analyzer):
    """Test detection aggregation across tenants."""
    query = {
        "collection": "orders",
        "command": "aggregate",
        "pipeline": [
            {
                "$group": {
                    "_id": "$status",
                    "total": {"$sum": "$amount"}
                }
            }
        ]
    }
    
    result = analyzer.analyze(query)
    
    assert result.ada_cross_tenant is True


def test_non_tenant_scoped_collection(analyzer):
    """Test collection yang tidak require tenant isolation."""
    query = {
        "collection": "system_config",
        "command": "find",
        "filter": {}
    }
    
    result = analyzer.analyze(query)
    
    # Collection ini tidak butuh tenant isolation
    assert result.ada_tenant_filter is True  # Not applicable
