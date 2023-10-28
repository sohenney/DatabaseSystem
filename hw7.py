import pymysql

db = pymysql.connect(
    host= "192.168.17.3",
    user= "madang",
    password= "madang",
    database= "madang",
    port=4567
    )

cursor = db.cursor()
cursor.execute("USE madang")

def get_schema(table_name):
    schema_query = f"DESCRIBE {table_name}"
    cursor.execute(schema_query)
    schema = cursor.fetchall()
    column_names = [row[0] for row in schema]
    return column_names

# 삽입 함수
def insert_data(table_name):
    print(f"데이터를 {table_name} 테이블에 삽입합니다.")
    column_names = get_schema(table_name)
    values = []

    for column_name in column_names:
        value = input(f"{column_name} 입력: ")
        values.append(value)

    placeholders = ', '.join(['%s'] * len(column_names))
    insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
    
    try:
        cursor.execute(insert_query, values)
        db.commit()
        print("데이터가 삽입되었습니다.")
    except Exception as e:
        db.rollback()
        print(f"삽입 오류 발생: {str(e)}")

# 삭제 함수
def delete_data(table_name):
    print(f"데이터를 {table_name} 테이블에서 삭제합니다.")
    delete_condition = input("삭제 조건 입력 (예: column1 = '조건', 전체 데이터를 삭제하려면 빈 칸 또는 '1' 입력): ")
    if delete_condition.strip() == "" or delete_condition == "1":
        delete_query = f"DELETE FROM {table_name}"
    else:
        delete_query = f"DELETE FROM {table_name} WHERE {delete_condition}"
    
    try:
        cursor.execute(delete_query)
        db.commit()
        print(f"데이터가 삭제되었습니다.")
    except Exception as e:
        db.rollback()
        print(f"삭제 오류 발생: {str(e)}")

# 검색 함수
def search_data(table_name):
    print(f"데이터를 {table_name} 테이블에서 검색합니다.")
    search_condition = input("검색 조건 입력 (예: column1 = '조건', 전체 데이터를 검색하려면 빈 칸 또는 '1' 입력): ")
    if search_condition.strip() == "" or search_condition == "1":
        search_query = f"SELECT * FROM {table_name}"
    else:
        search_query = f"SELECT * FROM {table_name} WHERE {search_condition}"
    
    try:
        cursor.execute(search_query)
        result = cursor.fetchall()
        for row in result:
            print(row)
    except Exception as e:
            print(f"검색 오류 발생: {str(e)}")


# 메인
if __name__ == "__main__":
    while True:
        print("1. 데이터 삽입")
        print("2. 데이터 삭제")
        print("3. 데이터 검색")
        print("4. 종료")
        choice = input("실행할 작업을 선택하세요. (1/2/3/4): ")

        if choice == "1":
            table_name= input("삽입할 테이블 이름 입력 (Book, Customer, Imported_Book, NewOrders, Orders): ")
            insert_data(table_name)
        elif choice == "2":
            table_name= input("삭제할 테이블 이름 입력 (Book, Customer, Imported_Book, NewOrders, Orders): ")
            delete_data(table_name)
        elif choice == "3":
            table_name= input("검색할 테이블 이름 입력 (Book, Customer, Imported_Book, NewOrders, Orders): ")
            search_data(table_name)
        elif choice == "4":
            break
        else:
            print("알 수 없는 번호입니다. 다시 입력하세요.")

db.close()
