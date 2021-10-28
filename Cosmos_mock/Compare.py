def compare_quota(A, B):
    if A.priorityX < B.priorityX:
        return -1
    if A.priorityX > B.priorityX:
        return 1
    if A.SLA is not None and B.SLA is None:
        return -1
    if A.SLA is None and B.SLA is not None:
        return 1
    if A.au.quota < 0 < B.au.quota:
        return 1
    if A.au.quota > 0 > B.au.quota:
        return -1
    if A.last_priority != B.last_priority:
        if A.last_priority < B.last_priority:
            return -1
        if A.last_priority > B.last_priority:
            return 1
    if A.submit_time < B.submit_time:
        return -1
    if B.submit_time > A.submit_time:
        return 1
    return 0


def compare_ML(A, B):
    return A.predict_priority - B.predict_priority
