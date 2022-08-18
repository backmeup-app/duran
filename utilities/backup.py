from datetime import datetime
import time

# Validation to make sure that not more than 1 backup
# has been made today for the resource
def is_backed_up_today(resource, backup_service):
    now = datetime.now()
    year = int(now.strftime("%Y"))
    month = int(now.strftime("%m"))
    day = int(now.strftime("%d"))
    start = datetime(year, month, day, 0, 0, 0)
    end = datetime(year, month, day, 23, 59, 59)
    backup = backup_service.find_one(
        {"resource": resource.get("_id"), "created_at": {"$gte": start, "$lte": end}}
    )
    return not bool(backup)
