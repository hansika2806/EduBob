"""
Monitoring and performance tracking utilities.
Provides metrics collection and health check functionality.
"""

import time
import psutil
import logging
from datetime import datetime, timezone
from typing import Dict, Any
from functools import wraps
from sqlalchemy import text
from database import engine

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """
    Performance monitoring utility for tracking API metrics.
    """
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.total_response_time = 0.0
        self.start_time = time.time()
    
    def record_request(self, response_time: float, is_error: bool = False):
        """Record a request with its response time"""
        self.request_count += 1
        self.total_response_time += response_time
        if is_error:
            self.error_count += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        uptime = time.time() - self.start_time
        avg_response_time = (
            self.total_response_time / self.request_count 
            if self.request_count > 0 else 0
        )
        
        return {
            "uptime_seconds": round(uptime, 2),
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "error_rate": round(self.error_count / self.request_count * 100, 2) if self.request_count > 0 else 0,
            "avg_response_time_ms": round(avg_response_time * 1000, 2)
        }


# Global performance monitor instance
performance_monitor = PerformanceMonitor()


def track_performance(func):
    """
    Decorator to track function performance.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        is_error = False
        
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            is_error = True
            raise
        finally:
            response_time = time.time() - start_time
            performance_monitor.record_request(response_time, is_error)
    
    return wrapper


def get_system_metrics() -> Dict[str, Any]:
    """
    Get current system resource usage metrics.
    
    Returns:
        Dictionary with CPU, memory, and disk usage
    """
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu_usage_percent": round(cpu_percent, 2),
            "memory_usage_percent": round(memory.percent, 2),
            "memory_available_mb": round(memory.available / (1024 * 1024), 2),
            "disk_usage_percent": round(disk.percent, 2),
            "disk_free_gb": round(disk.free / (1024 * 1024 * 1024), 2)
        }
    except Exception as e:
        logger.error(f"Failed to get system metrics: {str(e)}")
        return {
            "error": "Failed to retrieve system metrics"
        }


def check_database_health() -> Dict[str, Any]:
    """
    Check database connectivity and health.
    
    Returns:
        Dictionary with database health status
    """
    try:
        start_time = time.time()
        
        # Try to execute a simple query
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        
        response_time = time.time() - start_time
        
        # Get pool info (handle both QueuePool and StaticPool)
        pool_info = {}
        try:
            if hasattr(engine.pool, 'size'):
                pool_info["pool_size"] = engine.pool.size()
            if hasattr(engine.pool, 'checkedout'):
                pool_info["checked_out_connections"] = engine.pool.checkedout()
        except Exception:
            pool_info["pool_type"] = str(type(engine.pool).__name__)
        
        return {
            "status": "healthy",
            "response_time_ms": round(response_time * 1000, 2),
            **pool_info
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


def get_comprehensive_health() -> Dict[str, Any]:
    """
    Get comprehensive health check including all subsystems.
    
    Returns:
        Dictionary with complete health status
    """
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "healthy",  # Overall status
        "database": check_database_health(),
        "system": get_system_metrics(),
        "performance": performance_monitor.get_metrics()
    }

# Made with Bob