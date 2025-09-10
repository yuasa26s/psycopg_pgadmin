# psycopg_pgadmin(プログラミング練習_問題)
問題集の要件に基づき、CRUD処理を行い、その結果をCSVファイルに出力する4つの問題を作成します。以下がそれぞれの問題です。

1. Create処理
    - 問題: `employees`テーブルに新しい従業員のデータをINSERTしてください。新しい従業員のデータは以下の通りです。
        - `employee_id: 3, first_name: 'Alice', last_name: 'Smith', department: 'IT', salary: 55000`
    - 出力: INSERT処理が成功した場合は、「Success」というメッセージをCSVファイルに出力してください。失敗した場合は、「Failure」というメッセージを出力してください。
2. Read処理
    - 問題: `employees`テーブルから全ての従業員のデータをSELECTしてください。
    - 出力: SELECT結果をCSVファイルに出力してください。
3. Update処理
    - 問題: `employees`テーブルで`employee_id`が1の従業員の`salary`を60000にUPDATEしてください。
    - 出力: UPDATE処理が成功した場合は、「Success」というメッセージをCSVファイルに出力してください。失敗した場合は、「Failure」というメッセージを出力してください。
4. Delete処理
    - 問題: `employees`テーブルで`employee_id`が2の従業員のデータをDELETEしてください。
    - 出力: DELETE処理が成功した場合は、「Success」というメッセージをCSVファイルに出力してください。失敗した場合は、「Failure」というメッセージを出力してください。


## 生成されたCSVファイル
Windows側からもWSLパス経由でアクセス可能：
\\wsl$\kali-linux\home\pino26\git_test\psycopg_pgadmin\
├── create_result.csv    (Success + タイムスタンプ)
├── read_result.csv      (全従業員データ)
├── update_result.csv    (Success + タイムスタンプ) 
└── delete_result.csv    (Success + タイムスタンプ)

## 達成した目標
✅ psycopg2によるPostgreSQL接続
✅ pgAdmin4との連携可能な環境
✅ 完全なCRUD操作の実装
✅ CSV出力機能の実装
✅ エラーハンドリングの実装
✅ WSL環境での正常動作
すべての要件が完全に満たされました！
