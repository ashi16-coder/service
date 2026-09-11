import sqlite3

from inventory_app.repository import ProductRepository


def build_db():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            price REAL,
            active INTEGER
        )
        """
    )
    conn.executemany(
        "INSERT INTO products (name, category, price, active) VALUES (?, ?, ?, ?)",
        [
            ("Laptop", "Electronics", 999.0, 1),
            ("Mouse", "Electronics", 25.0, 1),
            ("Keyboard", "Electronics", 45.0, 1),
            ("Novel", "Books", 18.0, 1),
            ("Notebook", "Books", 12.0, 0),
            ("Desk", "Furniture", 300.0, 1),
        ],
    )
    conn.commit()
    return conn


def test_filters_execute_in_sql_and_return_matches():
    repo = ProductRepository(build_db())

    result = repo.list_products(filters={"category": "Electronics", "active": 1}, page=1, page_size=2)

    assert [item["name"] for item in result["items"]] == ["Laptop", "Mouse"]
    assert result["total"] == 3
    assert result["page"] == 1
    assert result["page_size"] == 2
    assert result["total_pages"] == 2


def test_empty_results_are_handled():
    repo = ProductRepository(build_db())

    result = repo.list_products(filters={"category": "Unknown"}, page=1, page_size=10)

    assert result["items"] == []
    assert result["total"] == 0
    assert result["total_pages"] == 0
    assert result["page"] == 1


def test_pagination_remains_correct_with_filters():
    repo = ProductRepository(build_db())

    result = repo.list_products(filters={"category": "Electronics"}, page=2, page_size=2)

    assert [item["name"] for item in result["items"]] == ["Keyboard"]
    assert result["total"] == 3
    assert result["page"] == 2
    assert result["page_size"] == 2
    assert result["total_pages"] == 2
