class BuildFixes:
    def __init__(self, id, number, status, build_type_id):
        self.id = id
        self.number = number
        self.status = status
        self.build_type_id = build_type_id
        self.fixed_references = []
        self.merged_references = []

    def add_fixed(self, youtrack_id):
        self.fixed_references.append(youtrack_id)

    def add_merged(self, youtrack_id):
        self.merged_references.append(youtrack_id)

    def extend_fixes(self, id_list):
        self.fixed_references.extend(id_list)

    def extend_merges(self, id_list):
        self.merged_references.extend(id_list)
