import csv, cStringIO

def to_csv(rows): 
    memory_file = cStringIO.StringIO()
    writer = csv.writer(memory_file, delimiter=',')
    writer.writerows(rows)
    output = memory_file.getvalue()
    memory_file.close()
    return output