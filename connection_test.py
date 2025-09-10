import psycopg2
try:
    connection = psycopg2.connect(
        host='localhost',
        database='testdb',
        user='postgres',
        password='Aya1126s',
        port=5432
)
    print("✅ データベース接続成功！")
    connection.close()
except Exception as e:
    print(f"❌ 接続エラー: {e}")
