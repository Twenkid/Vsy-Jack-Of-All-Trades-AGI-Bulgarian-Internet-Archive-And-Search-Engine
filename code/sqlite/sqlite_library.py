"""
SQLite Library for URL and Content Management
Provides database creation, schema management, data insertion, and comprehensive search functionality.
....
Claude ...

*** Sqlime - SQLite Playground
https://sqlime.org/#deta:m97q76wmvzvd
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pathlib import Path


class URLDatabase:
    """A library for managing URL and content data in SQLite."""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to database file. If None, creates in-memory database.
        """
        if db_path is None:
            self.db_path = ":memory:"
            self.conn = sqlite3.connect(":memory:")
        else:
            self.db_path = db_path
            self.conn = sqlite3.connect(db_path)
        
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self.cursor = self.conn.cursor()
    
    def create_schema(self):
        """Create the database schema with all required fields."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS url_data (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            URL VARCHAR(2048),
            URLID INTEGER,
            timestamp VARCHAR(50),
            year INTEGER,
            month INTEGER,
            day INTEGER,
            hour INTEGER,
            minute INTEGER,
            second INTEGER,
            millisecond INTEGER,
            label VARCHAR(255),
            category VARCHAR(255),
            html TEXT,
            text TEXT,
            summary1 TEXT,
            summary2 TEXT,
            continuation TEXT,
            notes1 TEXT,
            notes2 TEXT,
            connect TEXT,
            images INTEGER,
            filepaths TEXT,
            Links_List TEXT,
            Links_Text TEXT,
            Traverse_id INTEGER,
            Dereference INTEGER
        );
        """
        
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        print(f"Schema created successfully in database: {self.db_path}")
    
    def add_data(self, 
                 url: Optional[str] = None,
                 urlid: Optional[int] = None,   
                 timestamp: Optional[str] = None,
                 label: Optional[str] = None,
                 category: Optional[str] = None,
                 html: Optional[str] = None,
                 text: Optional[str] = None,
                 summary1: Optional[str] = None,
                 summary2: Optional[str] = None,
                 continuation: Optional[str] = None,
                 notes1: Optional[str] = None,
                 notes2: Optional[str] = None,
                 connect: Optional[str] = None,
                 images: Optional[int] = None,
                 filepaths: Optional[str] = None,
                 links_list: Optional[str] = None,
                 links_text: Optional[str] = None,
                 traverse_id: Optional[int] = None,
                 dereference: Optional[int] = None,
                 auto_timestamp: bool = True) -> int:
        """
        Add data to the database programmatically.
        
        Args:
            url: URL string
            urlid: URL ID integer
            timestamp: Custom timestamp string (if not provided and auto_timestamp=True, uses current time)
            label: Label string
            category: Category string
            html: HTML content
            text: Text content
            summary1: First summary
            summary2: Second summary
            continuation: Continuation text
            notes1: First notes field
            notes2: Second notes field
            connect: Connection information
            images: Image ID
            filepaths: File paths
            links_list: List of links
            links_text: Link text
            traverse_id: Traverse ID
            dereference: Dereference ID
            auto_timestamp: If True and timestamp is None, auto-generate timestamp
        
        Returns:
            The ID of the inserted row
        """
        # Auto-generate timestamp if needed
        if timestamp is None and auto_timestamp:
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Include milliseconds
            year = now.year
            month = now.month
            day = now.day
            hour = now.hour
            minute = now.minute
            second = now.second
            millisecond = now.microsecond // 1000
        elif timestamp:
            # Parse timestamp to extract components
            dt = datetime.strptime(timestamp.split('.')[0], "%Y-%m-%d %H:%M:%S")
            year = dt.year
            month = dt.month
            day = dt.day
            hour = dt.hour
            minute = dt.minute
            second = dt.second
            # Extract milliseconds if present
            if '.' in timestamp:
                millisecond = int(timestamp.split('.')[1][:3])
            else:
                millisecond = 0
        else:
            year = month = day = hour = minute = second = millisecond = None
        
        insert_sql = """
        INSERT INTO url_data (
            URL, URLID, timestamp, year, month, day, hour, minute, second, millisecond,
            label, category, html, text, summary1, summary2, continuation,
            notes1, notes2, connect, images, filepaths, Links_List, Links_Text,
            Traverse_id, Dereference
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        self.cursor.execute(insert_sql, (
            url, urlid, timestamp, year, month, day, hour, minute, second, millisecond,
            label, category, html, text, summary1, summary2, continuation,
            notes1, notes2, connect, images, filepaths, links_list, links_text,
            traverse_id, dereference
        ))
        
        self.conn.commit()
        return self.cursor.lastrowid
    
    # ============================================================================
    # SEARCH FUNCTIONS
    # ============================================================================
    
    def search_by_full_timestamp(self, timestamp: str) -> List[sqlite3.Row]:
        """
        Search for records matching exact timestamp.
        
        Args:
            timestamp: Timestamp string in format "YYYY-MM-DD HH:MM:SS.mmm"
        
        Returns:
            List of matching rows
        """
        query = "SELECT * FROM url_data WHERE timestamp = ?"
        self.cursor.execute(query, (timestamp,))
        return self.cursor.fetchall()
    
    def search_by_time_component(self, 
                                  year: Optional[int] = None,
                                  month: Optional[int] = None,
                                  day: Optional[int] = None,
                                  hour: Optional[int] = None,
                                  minute: Optional[int] = None,
                                  second: Optional[int] = None,
                                  millisecond: Optional[int] = None) -> List[sqlite3.Row]:
        """
        Search for records matching specific time components.
        
        Args:
            year: Year to search for
            month: Month to search for (1-12)
            day: Day to search for (1-31)
            hour: Hour to search for (0-23)
            minute: Minute to search for (0-59)
            second: Second to search for (0-59)
            millisecond: Millisecond to search for (0-999)
        
        Returns:
            List of matching rows
        """
        conditions = []
        params = []
        
        if year is not None:
            conditions.append("year = ?")
            params.append(year)
        if month is not None:
            conditions.append("month = ?")
            params.append(month)
        if day is not None:
            conditions.append("day = ?")
            params.append(day)
        if hour is not None:
            conditions.append("hour = ?")
            params.append(hour)
        if minute is not None:
            conditions.append("minute = ?")
            params.append(minute)
        if second is not None:
            conditions.append("second = ?")
            params.append(second)
        if millisecond is not None:
            conditions.append("millisecond = ?")
            params.append(millisecond)
        
        if not conditions:
            return []
        
        query = f"SELECT * FROM url_data WHERE {' AND '.join(conditions)}"
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def search_by_time_period(self, 
                               start_timestamp: str,
                               end_timestamp: str) -> List[sqlite3.Row]:
        """
        Search for records within a time period.
        
        Args:
            start_timestamp: Start of period (format: "YYYY-MM-DD HH:MM:SS.mmm")
            end_timestamp: End of period (format: "YYYY-MM-DD HH:MM:SS.mmm")
        
        Returns:
            List of matching rows
        """
        query = "SELECT * FROM url_data WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp"
        self.cursor.execute(query, (start_timestamp, end_timestamp))
        return self.cursor.fetchall()
    
    def search_in_field(self, 
                        field_name: str,
                        search_term: str,
                        exact_match: bool = False) -> List[sqlite3.Row]:
        """
        Search within a specific text field.
        
        Args:
            field_name: Name of the field to search in (html, text, label, category, etc.)
            search_term: Term to search for
            exact_match: If True, search for exact match. If False, use LIKE with wildcards.
        
        Returns:
            List of matching rows
        """
        valid_fields = [
            'html', 'text', 'label', 'category', 'summary1', 'summary2',
            'continuation', 'notes1', 'notes2', 'connect', 'filepaths',
            'Links_List', 'Links_Text', 'URL'
        ]
        
        if field_name not in valid_fields:
            raise ValueError(f"Invalid field name. Must be one of: {', '.join(valid_fields)}")
        
        if exact_match:
            query = f"SELECT * FROM url_data WHERE {field_name} = ?"
            self.cursor.execute(query, (search_term,))
        else:
            query = f"SELECT * FROM url_data WHERE {field_name} LIKE ?"
            self.cursor.execute(query, (f"%{search_term}%",))
        
        return self.cursor.fetchall()
    
    def search_multiple_fields(self,
                               search_term: str,
                               fields: Optional[List[str]] = None,
                               exact_match: bool = False) -> List[sqlite3.Row]:
        """
        Search across multiple fields simultaneously.
        
        Args:
            search_term: Term to search for
            fields: List of field names to search in. If None, searches all text fields.
            exact_match: If True, search for exact match. If False, use LIKE with wildcards.
        
        Returns:
            List of matching rows
        """
        if fields is None:
            fields = [
                'html', 'text', 'label', 'category', 'summary1', 'summary2',
                'continuation', 'notes1', 'notes2', 'connect', 'filepaths',
                'Links_List', 'Links_Text'
            ]
        
        if exact_match:
            conditions = [f"{field} = ?" for field in fields]
            query = f"SELECT * FROM url_data WHERE {' OR '.join(conditions)}"
            params = [search_term] * len(fields)
        else:
            conditions = [f"{field} LIKE ?" for field in fields]
            query = f"SELECT * FROM url_data WHERE {' OR '.join(conditions)}"
            params = [f"%{search_term}%" for _ in fields]
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_all_records(self) -> List[sqlite3.Row]:
        """Retrieve all records from the database."""
        self.cursor.execute("SELECT * FROM url_data")
        return self.cursor.fetchall()
    
    def get_record_by_id(self, record_id: int) -> Optional[sqlite3.Row]:
        """Retrieve a single record by ID."""
        self.cursor.execute("SELECT * FROM url_data WHERE ID = ?", (record_id,))
        return self.cursor.fetchone()
    
    def close(self):
        """Close the database connection."""
        self.conn.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_memory_db() -> URLDatabase:
    """Create an in-memory database."""
    db = URLDatabase()
    db.create_schema()
    return db


def create_file_db(filepath: str) -> URLDatabase:
    """Create a file-backed database."""
    db = URLDatabase(filepath)
    db.create_schema()
    return db


def print_results(results: List[sqlite3.Row]):
    """Pretty print search results."""
    if not results:
        print("No results found.")
        return
    
    print(f"\nFound {len(results)} result(s):\n")
    for row in results:
        print(f"ID: {row['ID']}")
        print(f"  URL: {row['URL']}")
        print(f"  Timestamp: {row['timestamp']}")
        print(f"  Label: {row['label']}")
        print(f"  Category: {row['category']}")
        if row['text']:
            preview = row['text'][:100] + "..." if len(row['text']) > 100 else row['text']
            print(f"  Text: {preview}")
        print("-" * 80)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example 1: In-memory database
    print("=== Example 1: In-memory Database ===")
    with create_memory_db() as db:
        # Add some sample data
        id1 = db.add_data(
            url="https://example.com/page1",
            urlid=1,
            label="Example Page",
            category="Documentation",
            text="This is some sample text content.",
            summary1="A brief summary of the page."
        )
        print(f"Inserted record with ID: {id1}")
        
        # Search example
        results = db.search_in_field("category", "Documentation")
        print_results(results)
    
    # Example 2: File-backed database
    print("\n=== Example 2: File-backed Database ===")
    with create_file_db("example.db") as db:
        # Add data with custom timestamp
        id2 = db.add_data(
            url="https://example.com/article",
            urlid=2,
            timestamp="2024-01-15 14:30:45.123",
            label="Article",
            category="News",
            text="Article content here",
            summary1="Article summary",
            notes1="Important article"
        )
        print(f"Inserted record with ID: {id2}")
        
        # Search by time component
        results = db.search_by_time_component(year=2024, month=1)
        print_results(results)
    
    print("\nDatabase examples completed successfully!")
