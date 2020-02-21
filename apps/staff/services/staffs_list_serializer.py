from random import shuffle
from ..models import Staff


class StaffsListSerializer:

    def __init__(self, query_set):
        self.staffs = list(query_set)
        self.group_titles = list(set([staff.group_title for staff in self.staffs]))
        self.serialized_data = {}

    def data(self):
        shuffle(self.staffs)
        self._partitioning_by_group_title()
        return self.serialized_data

    def _partitioning_by_group_title(self):
        for group_title in self.group_titles:
            self.serialized_data[group_title] = {}
            team_titles = list(set([staff.team_title for staff in self.staffs if staff.group_title == group_title]))
            for team_title in team_titles:
                staffs = [staff for staff in self.staffs if
                          staff.group_title == group_title and staff.team_title == team_title]
                self.serialized_data[group_title][team_title] = []
                for staff in staffs:
                    self.serialized_data[group_title][team_title].append({
                        'group_title': staff.group_title,
                        'team_title': staff.team_title,
                        'first_name_en': staff.first_name_en,
                        'first_name_fa': staff.first_name_fa,
                        'last_name_en': staff.last_name_en,
                        'last_name_fa': staff.last_name_fa,
                        'url': staff.url,
                        'image': staff.image.url
                    })
                self.staffs = [staff for staff in self.staffs if staff not in staffs]
