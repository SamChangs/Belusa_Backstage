# from dotenv import load_dotenv
# import databases, sqlalchemy
# import os
# load_dotenv()

# DATABASE_URL = os.getenv('PostgreSQL',default=None)
# database = databases.Database(DATABASE_URL)
# metadata = sqlalchemy.MetaData()


# admin = sqlalchemy.Table(
# "wb_admin",
# metadata,
# sqlalchemy.Column("storename", sqlalchemy.String),
# sqlalchemy.Column("account", sqlalchemy.String),
# sqlalchemy.Column("password", sqlalchemy.String)
# )

# engine = sqlalchemy.create_engine(
#     DATABASE_URL
# )

# metadata.create_all(engine)



