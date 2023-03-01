# The python DBAPI
# import psycopg
from sqlalchemy import Engine, create_engine, text
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
engine = create_engine("postgresql+psycopg://postgres:test123@localhost/turingbyte",future=True)

# print(type(engine))
conn = engine.connect()
conn1 = engine.begin()
# print(conn)
stmt = text("select * from users")
result = conn.execute(stmt)
# print(result.first())
row = result.first()
abc = result.all()
conn.commit()
conn.close()
print(row._mapping.keys())
print(row._mapping.items())



