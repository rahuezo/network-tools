from files.readers import FileReader
from files.sanitizer import sanitize_string
from entities import get_people

import tkFileDialog as fd
import pandas as pd


class EventBuilder: 
    @staticmethod
    def get_event_header(f, online=True): 
        if not online: 
            f = f.split('/')[-1]

        return sanitize_string(' '.join(f[::-1].split('.')[1:])[::-1].upper())

    @staticmethod
    def dict_to_rows(d): 
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in d.iteritems()]))
        df = df.fillna('')
        return [list(df.columns.values)] + df.values.tolist()

    def __init__(self, files): 
        self.files = files

    def build(self): 
        events = {}
        for f in self.files:             
            header = EventBuilder.get_event_header(f, online=False)
            text = FileReader(f).read()
            events[header] = get_people(text)
        return EventBuilder.dict_to_rows(events)


files = fd.askopenfilenames(title="Choose .txt and .docx files")

ev = EventBuilder(files)

print ev.build()
