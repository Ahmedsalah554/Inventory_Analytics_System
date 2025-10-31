from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def create_inventory_table():
    hook = PostgresHook(postgres_conn_id='postgres_default')

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS inventory (
        id SERIAL PRIMARY KEY,
        product_name VARCHAR(100),
        quantity INTEGER,
        warehouse VARCHAR(50)
    );
    """
    hook.run(create_table_sql)

    clear_data_sql = "DELETE FROM inventory;"
    hook.run(clear_data_sql)

    insert_data_sql = """
    INSERT INTO inventory (product_name, quantity, warehouse)
    VALUES
        ('Laptop', 10, 'Warehouse A'),
        ('Mouse', 50, 'Warehouse B'),
        ('Keyboard', 30, 'Warehouse A'),
        ('Monitor', 15, 'Warehouse B');
    """
    hook.run(insert_data_sql)
    print("✅ Inventory table created and sample data inserted successfully")

def generate_inventory_report():
    hook = PostgresHook(postgres_conn_id='postgres_default')
    sql_query = "SELECT * FROM inventory;"
    conn = hook.get_conn()
    df = pd.read_sql(sql_query, conn)
    conn.close()

    os.makedirs('/opt/airflow/data', exist_ok=True)
    df.to_csv('/opt/airflow/data/inventory_report.csv', index=False)
    print("✅ Inventory report saved to CSV")
    print(df)

def visualize_inventory():
    df = pd.read_csv('/opt/airflow/data/inventory_report.csv')
    plt.figure(figsize=(10,6))
    plt.bar(df['product_name'], df['quantity'], color='skyblue')
    plt.title('Inventory Quantity by Product', fontsize=16)
    plt.xlabel('Product')
    plt.ylabel('Quantity')
    plt.tight_layout()

    os.makedirs('/opt/airflow/data/plots', exist_ok=True)
    plot_path = f'/opt/airflow/data/plots/inventory_plot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"✅ Inventory plot saved: {plot_path}")

with DAG(
    'inventory_analytics_pipeline',
    default_args=default_args,
    description='Inventory Analytics Pipeline using PostgreSQL',
    schedule_interval='@daily',
    catchup=False,
    tags=['inventory', 'analytics']
) as dag:

    task_create_table = PythonOperator(
        task_id='create_inventory_table',
        python_callable=create_inventory_table
    )

    task_generate_report = PythonOperator(
        task_id='generate_inventory_report',
        python_callable=generate_inventory_report
    )

    task_visualize_inventory = PythonOperator(
        task_id='visualize_inventory',
        python_callable=visualize_inventory
    )

    # Dependencies
    task_create_table >> task_generate_report >> task_visualize_inventory
