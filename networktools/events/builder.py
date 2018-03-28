from files.readers import FileReader
from files.sanitizer import sanitize_string
from entities import get_people

import tkFileDialog as fd


class EventBuilder: 
    @staticmethod
    def get_event_header(f, online=True): 
        if not online: 
            f = f.split('/')[-1]

        return sanitize_string(' '.join(f[::-1].split('.')[1:])[::-1].upper())

    def __init__(self, files): 
        self.files = files

    def build(self): 
        events = {}  # header: [list of people]

        for f in self.files:             
            header = EventBuilder.get_event_header(f, online=False)

            print header

            text = FileReader(f).read()

            events[header] = get_people(text)

        return events


files = fd.askopenfilenames(title="Choose .txt and .docx files")

ev = EventBuilder(files)

print ev.build()
