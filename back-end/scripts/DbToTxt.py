import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# SQL 쿼리 실행
cursor.execute("SELECT * FROM products_rentloanproduct")

# 결과 가져오기
rows = cursor.fetchall()

# 텍스트 파일로 저장
with open('accounts/fixtures/accounts/db_data.json', 'w', encoding='utf-8') as f:
    for row in rows:
        f.write(','.join(str(col) for col in row) + '\n')

# 연결 종료
conn.close()