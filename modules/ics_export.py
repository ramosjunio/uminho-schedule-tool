import hashlib
import re
from datetime import timezone

import ics

from lesson import Lesson
from modules.base import BaseExportModule


class IcsExportModule(BaseExportModule):
    """
    The ICS export module supports the following config options:
        - file_name: Exported file name
        - override_file: Replace data on existing ICS file (useful for updating a single day/week)
    """

    file_name = "./export/out.ics"
    override_file = None

    def __init__(self, config: dict):
        super().__init__()
        self.file_name = config["file_name"]
        self.override_file = config.get("override_file")

    @staticmethod
    def lesson_key(l: Lesson):
        return (
            l.name,
            l.shift,
            l.location,
            l.start.astimezone(timezone.utc),
            l.end.astimezone(timezone.utc),
        )

    @staticmethod
    def lesson_uid(l: Lesson) -> str:
        """
        Generate a deterministic, stable UID for RFC 5545 compliance.
        Ensures Google Calendar recognizes the same class across weekly runs.
        """
        raw_id = f"{l.name}_{l.shift}_{l.start.astimezone(timezone.utc).isoformat()}"
        digest = hashlib.sha1(raw_id.encode("utf-8")).hexdigest()
        return f"{digest}@uminho-schedule"

    @staticmethod
    def lesson_short_id(l: Lesson) -> str:
        """
        Generate a clean, human-readable ID for personal reference (e.g. in Notion).
        Examples:
          - 'Comportamento do Consumidor' -> 'CC-PL2-20260915-0830'
          - 'Investigação Operacional'    -> 'IO-TP1-20260915-0830'
          - 'Marketing Digital'           -> 'MD-TP1-20260915-1400'
        """
        # Extract meaningful initials from the course name (ignoring prepositions)
        words = [
            w
            for w in re.sub(r"[^\w\s]", "", l.name).split()
            if w.lower() not in {"de", "do", "da", "dos", "das", "e", "em"}
        ]
        if len(words) > 1:
            course_code = "".join(w[0] for w in words[:4]).upper()
        elif words:
            course_code = words[0][:4].upper()
        else:
            course_code = "CLASS"

        shift_clean = re.sub(r"\s+", "", l.shift)
        date_str = l.start.strftime("%Y%m%d-%H%M")
        return f"{course_code}-{shift_clean}-{date_str}"

    def export(self, lessons: list[Lesson]):
        print("Exporting to ICS...")

        if self.override_file:
            with open(self.override_file) as f:
                calendar = ics.Calendar(f.read())
        else:
            calendar = ics.Calendar()

        new_lessons = {self.lesson_key(l): l for l in lessons}

        existing_events = {
            (
                e.name,
                e.description,
                e.location,
                e.begin.astimezone(timezone.utc),
                e.end.astimezone(timezone.utc),
            ): e
            for e in calendar.events
        }

        keep_keys = set(existing_events.keys()) & set(new_lessons.keys())
        add_keys = set(new_lessons.keys()) - set(existing_events.keys())

        updated_events = {k: existing_events[k] for k in keep_keys}

        for k in add_keys:
            l = new_lessons[k]
            short_id = self.lesson_short_id(l)

            # Visible description in Google Calendar
            event_description = f"Shift: {l.shift}\nID: {short_id}"

            event = ics.Event(
                name=l.name,
                description=event_description,
                location=l.location,
                begin=l.start.astimezone(timezone.utc),
                end=l.end.astimezone(timezone.utc),
                uid=self.lesson_uid(l),
            )
            updated_events[k] = event

        calendar.events = set(updated_events.values())

        output_file = self.override_file if self.override_file else self.file_name
        with open(output_file, "w") as f:
            f.writelines(calendar.serialize_iter())