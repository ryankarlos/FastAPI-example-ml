from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData

graph = create_schema_graph(metadata=MetaData('postgres://user:pwd@host/database'))
graph.write_png('my_erd.png')