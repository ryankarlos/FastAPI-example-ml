from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph

graph = create_schema_graph(metadata=MetaData("postgresql://hello_fastapi:hello_fastapi@db/hello_fastapi_dev"))
graph.write_png("my_erd.png")
