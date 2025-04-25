from typing import List
from dataclasses import dataclass
from task_log.models.base_model import BaseModel
from task_log.utils.time_validator import (
    validate_date_string,
    validate_time_range,
    validate_time_string,
)


@dataclass
class Record(BaseModel):
    id: int
    date: str
    task_id: int
    description: str
    estimate_minutes: int
    start_time: str
    end_time: str = None
    actual_minutes: int = None
    note: str = None

    def __post_init__(self):
        validate_date_string(self.date, "date")
        self._validate_string(self.description, "description", max_length=300)
        validate_time_string(self.start_time, "start_time")
        if self.end_time:
            validate_time_string(self.end_time, "end_time")
            if self.start_time:
                validate_time_range(self.start_time, self.end_time)
                self._calculate_actual_minutes()
                self._validate_positive_integer(self.actual_minutes, "estimate_minutes")
        if self.note:
            self._validate_string(self.note, "note", max_length=300)

    def _calculate_actual_minutes(self):
        start_h, start_m = map(int, self.start_time.split(":"))
        end_h, end_m = map(int, self.end_time.split(":"))
        start_total = start_h * 60 + start_m
        end_total = end_h * 60 + end_m
        if end_total >= start_total:
            self.actual_minutes = end_total - start_total
        else:
            self._time_crosses_midnight(start_total, end_total)

    def _time_crosses_midnight(self, start_total, end_total):
        self.actual_minutes = (24 * 60 - start_total) + end_total

    @staticmethod
    def get_table_string(items: List["Record"]) -> str:
        columns = [
            ("Id", "id", int),
            ("Date", "date"),
            ("Task Id", "task_id", int),
            ("Description", "description"),
            ("Estimate", "estimate_minutes", str),
            ("StartTime", "start_time", str),
            ("EndTime", "end_time", str),
            ("ActualMinutes", "actual_minutes", str),
            ("Note", "note", str),
        ]
        return Record.generate_table_string(items, columns)
