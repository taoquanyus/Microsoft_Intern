class AU:
    maps = {}

    def __init__(self, au_id, quota, parent_au_id, au_hierarchy):
        self.au_id = au_id
        self.quota = quota
        self.parent_au_id = parent_au_id
        self.running_token = 0
        self.child_au = []
        self.parent_au = None
        self.au_hierarchy = au_hierarchy
        self.is_fully = 0
        AU.maps[au_id] = self

    def add_child(self, au):
        self.child_au.append(au)

    def remove_child(self, au):
        self.child_au.remove(au)

    def get_hierarchy(self):
        return self.au_hierarchy

    def find_au(self, au_id):
        if self.au_id == au_id:
            return self
        for au in self.child_au:
            ret = au.find_au(au_id)
            if ret is not None:
                return ret
        return None
