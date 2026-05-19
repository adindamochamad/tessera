"""
Query Analyzer Module

Module ini menganalisis MongoDB query patterns untuk detect
potential tenant isolation violations.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import re


@dataclass
class QueryAnalysisResult:
    """Hasil analisis query."""
    
    koleksi: str
    operasi: str  # "find", "aggregate", "update", dll
    ada_tenant_filter: bool
    field_tenant: Optional[str] = None
    ada_cross_tenant: bool = False
    pattern_violations: List[str] = None
    
    def __post_init__(self):
        if self.pattern_violations is None:
            self.pattern_violations = []


class MongoDBQueryAnalyzer:
    """
    Analyzer untuk MongoDB queries.
    
    Mendeteksi patterns yang menunjukkan potential data isolation issues.
    """
    
    # Collections yang require tenant isolation
    TENANT_SCOPED_COLLECTIONS = {
        "orders",
        "users",
        "analytics_events",
        "invoices",
        "products",
        "customers"
    }
    
    # Field names umum untuk tenant ID
    TENANT_FIELD_NAMES = {
        "tenant_id",
        "tenantId",
        "tenant",
        "organization_id",
        "org_id",
        "company_id"
    }
    
    def analyze(self, query: Dict[str, Any]) -> QueryAnalysisResult:
        """
        Analyze single MongoDB query.
        
        Args:
            query: Query object dari MongoDB
            
        Returns:
            QueryAnalysisResult dengan detection results
        """
        koleksi = query.get("collection", "unknown")
        operasi = query.get("command", "unknown")
        filter_obj = query.get("filter", {})
        
        # Check apakah collection butuh tenant isolation
        butuh_isolation = koleksi in self.TENANT_SCOPED_COLLECTIONS
        
        if not butuh_isolation:
            # Collection tidak require tenant isolation
            return QueryAnalysisResult(
                koleksi=koleksi,
                operasi=operasi,
                ada_tenant_filter=True  # Not applicable
            )
        
        # Check apakah ada tenant filter
        ada_tenant_filter, field_tenant = self._check_tenant_filter(filter_obj)
        
        # Check cross-tenant operations
        ada_cross_tenant = self._check_cross_tenant(query)
        
        # Detect violation patterns
        violations = []
        if not ada_tenant_filter:
            violations.append("missing_tenant_filter")
        if ada_cross_tenant:
            violations.append("cross_tenant_operation")
        
        return QueryAnalysisResult(
            koleksi=koleksi,
            operasi=operasi,
            ada_tenant_filter=ada_tenant_filter,
            field_tenant=field_tenant,
            ada_cross_tenant=ada_cross_tenant,
            pattern_violations=violations
        )
    
    def _check_tenant_filter(
        self,
        filter_obj: Dict[str, Any]
    ) -> tuple[bool, Optional[str]]:
        """
        Check apakah filter object contains tenant ID.
        
        Returns:
            (ada_filter, field_name)
        """
        for field_name in self.TENANT_FIELD_NAMES:
            if field_name in filter_obj:
                return (True, field_name)
        
        # Check di dalam $and, $or conditions
        if "$and" in filter_obj:
            for condition in filter_obj["$and"]:
                ada, field = self._check_tenant_filter(condition)
                if ada:
                    return (ada, field)
        
        if "$or" in filter_obj:
            # $or adalah risky - bisa bypass tenant isolation
            # Tapi bisa jadi valid kalau semua branches ada tenant filter
            pass
        
        return (False, None)
    
    def _check_cross_tenant(self, query: Dict[str, Any]) -> bool:
        """
        Check apakah query melakukan cross-tenant operations.
        
        Contoh: $lookup ke collection lain tanpa tenant filter
        """
        # Check aggregation pipeline
        pipeline = query.get("pipeline", [])
        
        for stage in pipeline:
            # Check $lookup stage
            if "$lookup" in stage:
                lookup = stage["$lookup"]
                # TODO: Check apakah lookup preserves tenant boundaries
                # Ini complex - butuh analyze join conditions
                pass
            
            # Check $group stage
            if "$group" in stage:
                group = stage["$group"]
                # Kalau group by bukan tenant_id, bisa aggregate across tenants
                if "_id" in group:
                    group_field = group["_id"]
                    if isinstance(group_field, str):
                        if not any(
                            tenant_field in group_field 
                            for tenant_field in self.TENANT_FIELD_NAMES
                        ):
                            return True  # Potential cross-tenant aggregation
        
        return False


# Singleton instance
query_analyzer = MongoDBQueryAnalyzer()
