from fastapi import FastAPI,Path


app=FastAPI()

students={
    1:{
        "name":"Mahabub",
        "age":17,
        "class":"Inter 2nd Year"
    },
    2:{
        "name":"Mak",
        "age":9,
        "class":"Inter 1nd Year"
    },
    3:{
        "name":"shamol",
        "age":22,
        "class":"Inter Year"
    },
    4:{
        "name":"Rahman",
        "age":22,
        "class":"Inter 3rd Year"
    }
}

@app.get('/')
def get():
    return {"hello":"world"}

@app.get('/get-student/{student_id}')
def get_students(students_id:int=Path(None,description="The id of the student you want to view",gt=0,lt=7)):
    return students[students_id]