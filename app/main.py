from fastapi import FastAPI
from dotenv import load_dotenv
import database, models
from routers import post, user, auth

load_dotenv()

models.create_table(database.engine)

app = FastAPI()

# class Post(BaseModel):
    # title: str
    # content: str

'''
This is a connection setup using psycopg, since we shifted to SQLModel to connect to DB and execute query using ORM,
this piece of code is not required.
while True:
    try:
        conn = psycopg.connect(f"host={os.environ["DB_HOST"]} dbname={os.environ["DB_NAME"]} user={os.environ["DB_USER"]} password={os.environ["DB_PASSWORD"]}", row_factory=dict_row) # as conn:
        cur = conn.cursor() # as cur:
        break
    except Exception as error:
        print("Connection to database if faild with error: ", error)
        time.sleep(2)
'''


# API

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "Welcome to the social media"}