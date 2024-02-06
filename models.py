# Example models.py content:
class User:
    def _init_(self, username, password, unique_id):
        self.username = username
        self.password = password
        self.unique_id = unique_id

class Relationship:
    def _init_(self, partner1_id, partner2_id, start_date, milestones):
        self.partner1_id = partner1_id
        self.partner2_id = partner2_id
        self.start_date = start_date
        self.milestones = milestones
