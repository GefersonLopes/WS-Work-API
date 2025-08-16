from flask import request

def get_pagination_defaults():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        page, limit = 1, 10
    page = max(1, page)
    limit = max(1, min(100, limit))
    return page, limit, request.args.get("search", None)
