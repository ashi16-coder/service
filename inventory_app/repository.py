class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def list_products(self, filters=None, page=1, page_size=10):
        filters = filters or {}

        clauses = []
        values = []
        for key, value in filters.items():
            clauses.append(f"{key} = ?")
            values.append(value)

        where_sql = ""
        if clauses:
            where_sql = " WHERE " + " AND ".join(clauses)

        total_query = f"SELECT COUNT(*) FROM products{where_sql}"
        total = self.conn.execute(total_query, values).fetchone()[0]

        if total == 0:
            return {
                "items": [],
                "total": 0,
                "page": page,
                "page_size": page_size,
                "total_pages": 0,
            }

        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10

        offset = (page - 1) * page_size
        query = (
            f"SELECT id, name, category, price, active FROM products{where_sql} "
            "ORDER BY id LIMIT ? OFFSET ?"
        )
        rows = self.conn.execute(query, values + [page_size, offset]).fetchall()

        items = [
            {
                "id": row[0],
                "name": row[1],
                "category": row[2],
                "price": row[3],
                "active": bool(row[4]),
            }
            for row in rows
        ]

        total_pages = (total + page_size - 1) // page_size

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }
