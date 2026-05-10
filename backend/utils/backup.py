"""
Database backup utilities.
Provides automated backup functionality for SQLite database.
"""

import os
import shutil
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import gzip

logger = logging.getLogger(__name__)

# Backup configuration
BACKUP_DIR = os.getenv("BACKUP_DIR", "./backups")
MAX_BACKUPS = int(os.getenv("MAX_BACKUPS", "7"))  # Keep last 7 backups


def ensure_backup_directory():
    """Ensure backup directory exists"""
    Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)


def create_backup(db_path: str = "./edubob.db", compress: bool = True) -> Optional[str]:
    """
    Create a backup of the database.
    
    Args:
        db_path: Path to the database file
        compress: Whether to compress the backup with gzip
    
    Returns:
        Path to the backup file, or None if backup failed
    """
    try:
        ensure_backup_directory()
        
        # Check if database exists
        if not os.path.exists(db_path):
            logger.error(f"Database file not found: {db_path}")
            return None
        
        # Generate backup filename with timestamp
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_filename = f"edubob_backup_{timestamp}.db"
        
        if compress:
            backup_filename += ".gz"
        
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        
        # Create backup
        if compress:
            # Compress while copying
            with open(db_path, 'rb') as f_in:
                with gzip.open(backup_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        else:
            # Simple copy
            shutil.copy2(db_path, backup_path)
        
        logger.info(f"Database backup created: {backup_path}")
        
        # Clean up old backups
        cleanup_old_backups()
        
        return backup_path
        
    except Exception as e:
        logger.error(f"Failed to create backup: {str(e)}")
        return None


def cleanup_old_backups():
    """
    Remove old backups, keeping only the most recent MAX_BACKUPS files.
    """
    try:
        ensure_backup_directory()
        
        # Get all backup files
        backup_files = []
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith("edubob_backup_"):
                filepath = os.path.join(BACKUP_DIR, filename)
                backup_files.append((filepath, os.path.getmtime(filepath)))
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # Remove old backups
        if len(backup_files) > MAX_BACKUPS:
            for filepath, _ in backup_files[MAX_BACKUPS:]:
                try:
                    os.remove(filepath)
                    logger.info(f"Removed old backup: {filepath}")
                except Exception as e:
                    logger.error(f"Failed to remove old backup {filepath}: {str(e)}")
        
    except Exception as e:
        logger.error(f"Failed to cleanup old backups: {str(e)}")


def restore_backup(backup_path: str, db_path: str = "./edubob.db") -> bool:
    """
    Restore database from a backup file.
    
    Args:
        backup_path: Path to the backup file
        db_path: Path where to restore the database
    
    Returns:
        True if restore was successful, False otherwise
    """
    try:
        if not os.path.exists(backup_path):
            logger.error(f"Backup file not found: {backup_path}")
            return False
        
        # Create a backup of current database before restoring
        if os.path.exists(db_path):
            current_backup = f"{db_path}.before_restore"
            shutil.copy2(db_path, current_backup)
            logger.info(f"Created safety backup: {current_backup}")
        
        # Restore from backup
        if backup_path.endswith('.gz'):
            # Decompress while restoring
            with gzip.open(backup_path, 'rb') as f_in:
                with open(db_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        else:
            # Simple copy
            shutil.copy2(backup_path, db_path)
        
        logger.info(f"Database restored from: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to restore backup: {str(e)}")
        return False


def list_backups() -> list:
    """
    List all available backups.
    
    Returns:
        List of dictionaries with backup information
    """
    try:
        ensure_backup_directory()
        
        backups = []
        for filename in os.listdir(BACKUP_DIR):
            if filename.startswith("edubob_backup_"):
                filepath = os.path.join(BACKUP_DIR, filename)
                stat = os.stat(filepath)
                
                backups.append({
                    "filename": filename,
                    "path": filepath,
                    "size_bytes": stat.st_size,
                    "size_mb": round(stat.st_size / (1024 * 1024), 2),
                    "created_at": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                    "compressed": filename.endswith('.gz')
                })
        
        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x['created_at'], reverse=True)
        
        return backups
        
    except Exception as e:
        logger.error(f"Failed to list backups: {str(e)}")
        return []


def get_backup_info() -> dict:
    """
    Get information about backup system.
    
    Returns:
        Dictionary with backup system information
    """
    backups = list_backups()
    
    total_size = sum(b['size_bytes'] for b in backups)
    
    return {
        "backup_directory": BACKUP_DIR,
        "max_backups": MAX_BACKUPS,
        "total_backups": len(backups),
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "backups": backups
    }

# Made with Bob