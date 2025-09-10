import psycopg2
import csv
import os
from datetime import datetime

# CSV出力先ディレクトリ
CSV_OUTPUT_DIR = r"\\wsl$\kali-linux\home\pino26\git_test\psycopg_pgadmin"

class PostgreSQLCRUD:
    def __init__(self, host, database, user, password, port=5432):
        """PostgreSQLデータベースへの接続設定"""
        self.host = 'localhost',
        self.database = 'testdb',
        self.user = 'postgres',
        self.password = 'Aya1126s',
        self.port = '5432',
        self.connection = None
        self.cursor = None
        
        # CSV出力ディレクトリが存在しない場合は作成
        if not os.path.exists(CSV_OUTPUT_DIR):
            try:
                os.makedirs(CSV_OUTPUT_DIR)
                print(f"出力ディレクトリを作成しました: {CSV_OUTPUT_DIR}")
            except Exception as e:
                print(f"ディレクトリ作成エラー: {e}")
                print("カレントディレクトリに出力します")
    
    def connect(self):
        """データベースに接続"""
        try:
            self.connection = psycopg2.connect(
                host='localhost',
                database='testdb',
                user='postgres',
                password='Aya1126s',
                port=5432
            )
            self.cursor = self.connection.cursor()
            print("データベース接続成功")
            return True
        except psycopg2.Error as e:
            print(f"データベース接続エラー: {e}")
            return False
    
    def disconnect(self):
        """データベース接続を閉じる"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("データベース接続を閉じました")
    
    def create_employee(self, employee_id, first_name, last_name, department, salary):
        """Create処理: 新しい従業員データをINSERT"""
        try:
            insert_query = """
            INSERT INTO employees (employee_id, first_name, last_name, department, salary)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (employee_id, first_name, last_name, department, salary))
            self.connection.commit()
            
            # 結果をCSVファイルに出力
            filepath = os.path.join(CSV_OUTPUT_DIR, 'create_result.csv')
            self.write_result_to_csv(filepath, 'Success')
            print(f"従業員ID {employee_id} のデータを正常にINSERTしました")
            return True
            
        except psycopg2.Error as e:
            print(f"INSERT エラー: {e}")
            self.connection.rollback()
            filepath = os.path.join(CSV_OUTPUT_DIR, 'create_result.csv')
            self.write_result_to_csv(filepath, 'Failure')
            return False
    
    def read_employees(self):
        """Read処理: 全従業員データをSELECT"""
        try:
            select_query = "SELECT * FROM employees"
            self.cursor.execute(select_query)
            results = self.cursor.fetchall()
            
            # 列名を取得
            column_names = [desc[0] for desc in self.cursor.description]
            
            # 結果をCSVファイルに出力
            filepath = os.path.join(CSV_OUTPUT_DIR, 'read_result.csv')
            self.write_employees_to_csv(filepath, column_names, results)
            print(f"{len(results)}件の従業員データを取得しました")
            return results
            
        except psycopg2.Error as e:
            print(f"SELECT エラー: {e}")
            return None
    
    def update_employee_salary(self, employee_id, new_salary):
        """Update処理: 従業員の給与をUPDATE"""
        try:
            update_query = """
            UPDATE employees 
            SET salary = %s 
            WHERE employee_id = %s
            """
            self.cursor.execute(update_query, (new_salary, employee_id))
            
            if self.cursor.rowcount > 0:
                self.connection.commit()
                filepath = os.path.join(CSV_OUTPUT_DIR, 'update_result.csv')
                self.write_result_to_csv(filepath, 'Success')
                print(f"従業員ID {employee_id} の給与を{new_salary}に更新しました")
                return True
            else:
                filepath = os.path.join(CSV_OUTPUT_DIR, 'update_result.csv')
                self.write_result_to_csv(filepath, 'Failure')
                print(f"従業員ID {employee_id} が見つかりませんでした")
                return False
                
        except psycopg2.Error as e:
            print(f"UPDATE エラー: {e}")
            self.connection.rollback()
            filepath = os.path.join(CSV_OUTPUT_DIR, 'update_result.csv')
            self.write_result_to_csv(filepath, 'Failure')
            return False
    
    def delete_employee(self, employee_id):
        """Delete処理: 従業員データをDELETE"""
        try:
            delete_query = "DELETE FROM employees WHERE employee_id = %s"
            self.cursor.execute(delete_query, (employee_id,))
            
            if self.cursor.rowcount > 0:
                self.connection.commit()
                filepath = os.path.join(CSV_OUTPUT_DIR, 'delete_result.csv')
                self.write_result_to_csv(filepath, 'Success')
                print(f"従業員ID {employee_id} のデータを削除しました")
                return True
            else:
                filepath = os.path.join(CSV_OUTPUT_DIR, 'delete_result.csv')
                self.write_result_to_csv(filepath, 'Failure')
                print(f"従業員ID {employee_id} が見つかりませんでした")
                return False
                
        except psycopg2.Error as e:
            print(f"DELETE エラー: {e}")
            self.connection.rollback()
            filepath = os.path.join(CSV_OUTPUT_DIR, 'delete_result.csv')
            self.write_result_to_csv(filepath, 'Failure')
            return False
    
    def write_result_to_csv(self, filepath, result):
        """処理結果をCSVファイルに書き込み"""
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Result', 'Timestamp'])
                writer.writerow([result, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            print(f"結果をCSVファイルに出力しました: {filepath}")
        except Exception as e:
            print(f"CSV書き込みエラー: {e}")
            # フォールバック: カレントディレクトリに出力
            try:
                filename = os.path.basename(filepath)
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Result', 'Timestamp'])
                    writer.writerow([result, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                print(f"カレントディレクトリに出力しました: {filename}")
            except Exception as fallback_error:
                print(f"フォールバック出力もエラー: {fallback_error}")
    
    def write_employees_to_csv(self, filepath, column_names, data):
        """従業員データをCSVファイルに書き込み"""
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(column_names)  # ヘッダー行
                writer.writerows(data)  # データ行
            print(f"従業員データをCSVファイルに出力しました: {filepath}")
        except Exception as e:
            print(f"CSV書き込みエラー: {e}")
            # フォールバック: カレントディレクトリに出力
            try:
                filename = os.path.basename(filepath)
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(column_names)  # ヘッダー行
                    writer.writerows(data)  # データ行
                print(f"カレントディレクトリに出力しました: {filename}")
            except Exception as fallback_error:
                print(f"フォールバック出力もエラー: {fallback_error}")
    
    def create_employees_table(self):
        """テスト用のemployeesテーブルを作成（存在しない場合）"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS employees (
                employee_id INTEGER PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                department VARCHAR(50),
                salary INTEGER
            )
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("employeesテーブルを作成しました（既存の場合はスキップ）")
            
            # 初期データを挿入（テスト用）
            initial_data_query = """
            INSERT INTO employees (employee_id, first_name, last_name, department, salary)
            VALUES 
                (1, 'John', 'Doe', 'HR', 50000),
                (2, 'Jane', 'Brown', 'Finance', 55000)
            ON CONFLICT (employee_id) DO NOTHING
            """
            self.cursor.execute(initial_data_query)
            self.connection.commit()
            print("初期データを挿入しました")
            
        except psycopg2.Error as e:
            print(f"テーブル作成エラー: {e}")


def main():
    # データベース接続情報（実際の環境に合わせて変更してください）
    db_config = {
        'host': 'localhost',        # pgAdmin4で設定したホスト
        'database': 'testdb',       # データベース名
        'user': 'postgres',         # ユーザー名
        'password': 'Aya1126s',     # パスワード
        'port': 5432               # ポート番号
    }
    
    # PostgreSQLCRUDインスタンスを作成
    db = PostgreSQLCRUD(**db_config)
    
    try:
        # データベースに接続
        if not db.connect():
            return
        
        # テーブル作成（テスト用）
        db.create_employees_table()
        
        print("\n=== CRUD操作を開始します ===\n")
        
        # 1. Create処理
        print("1. Create処理")
        db.create_employee(3, 'Alice', 'Smith', 'IT', 55000)
        
        # 2. Read処理
        print("\n2. Read処理")
        employees = db.read_employees()
        
        # 3. Update処理
        print("\n3. Update処理")
        db.update_employee_salary(1, 60000)
        
        # 4. Delete処理
        print("\n4. Delete処理")
        db.delete_employee(2)
        
        print("\n=== 全ての操作が完了しました ===")
        print(f"以下のCSVファイルが {CSV_OUTPUT_DIR} に生成されました:")
        print("- create_result.csv (Create処理結果)")
        print("- read_result.csv (Read処理結果)")
        print("- update_result.csv (Update処理結果)")
        print("- delete_result.csv (Delete処理結果)")
        
    except Exception as e:
        print(f"実行中にエラーが発生しました: {e}")
    
    finally:
        # データベース接続を閉じる
        db.disconnect()


if __name__ == "__main__":
    main()