def paginate(query, page, per_page):
    total = query.count()
    items = query.paginate(page=page, per_page=per_page, error_out=False).items
    return {
        "items": [item.to_dict() for item in items],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
    }