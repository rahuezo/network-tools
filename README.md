# networktools
A set of tools for building/comparing networks (adjacency matrices) from events files, and node pairs files.

## Included Packages
1. networktools.events
2. networktools.files
3. networktools.matrices

#### Create Events File (using *EventBuilder* from *networktools.events.builder*)
EventBuilder takes as input a list of filepaths. These files can be either .docx or .txt.
`event_builder_instance.build()` creates a list of rows that can be iterated to write to csv file. 

```python
event_builder_instance = EventBuilder(list_of_filepaths)
rows = event_builder_instance.build()
```

#### Create Networks (adjacency matrices) from Events or Node Pairs Files (using *AdjacencyMatrix* from *networktools.matrices.matrices*)
