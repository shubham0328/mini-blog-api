from datetime import datetime   #import datetime for utc timestamp -> created_at

# static user list (hardcoded token auth)
USERS = [
    {"id": 1, "name": "Shubham", "token": "abc123"},
]

# hold blog posts and comments as dictonaries through API calls
POSTS = []
COMMENTS = []

# simple id counters for the post & comment (because we don't have a database to auto-generate id's)
_next_post_id = 1
_next_comment_id = 1


# Creates UTC timestamp -> (created_at)
def _now():
    """Return current UTC timestamp in ISO format (e.g. 2025-09-24T10:00:00Z)."""
    return datetime.utcnow().isoformat() + "Z"


# id generator function for getting next post
def get_next_post_id():
    """Return next post id (auto-increment)."""
    global _next_post_id
    nid = _next_post_id
    _next_post_id += 1
    return nid


# id generator function for getting next comment
def get_next_comment_id():
    """Return next comment id (auto-increment)."""
    global _next_comment_id
    nid = _next_comment_id
    _next_comment_id += 1
    return nid
