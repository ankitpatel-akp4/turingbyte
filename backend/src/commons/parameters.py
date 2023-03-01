

def page(offset: int = 0, limit: int = 10):
    return {"offset": offset, "limit": limit}
def filter(id: int = None, scope: str = None):
    return {"id": id, "scope": scope}
def sort():
    return "+id"

