import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS")
}

# Conecta ao banco
conn = psycopg2.connect(**config)

# Nome da tabela que você quer ler
table_name = os.getenv("TKT_RATED")

# 🔹 Lendo diretamente a tabela do banco
df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

# 🔧 Normalizar colunas
df.columns = df.columns.str.strip().str.lower()
print("Colunas detectadas:", df.columns.tolist())

# 🔧 Converter INTERVAL -> horas (float)
if "timetoresolve" in df.columns:
    df["timetoresolve"] = pd.to_timedelta(df["timetoresolve"]).dt.total_seconds() / 3600

# 2. Features numéricas
features = [
    "totalinteractions", "slachangecount", "iscritical", "timetoresolve"
]

X = df[features]
y = df["total_rating"]

# 3. Pré-processamento
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Split treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Modelo (Random Forest)
model = RandomForestClassifier(
    n_estimators=4, random_state=42
)
model.fit(X_train, y_train)

# 6. Avaliação
y_pred = model.predict(X_test)

testName = input("Nome do teste: ")

output_dir = os.path.join("reports", testName)
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, f"{testName}_description.txt"), "w") as f:
    f.write(f"Colunas analisadas: {features}\n")
    f.write(f"Total de linhas no dataset: {len(df)}\n")

confusion_matrix_ = confusion_matrix(y_test, y_pred)
classification_report_report_df = pd.DataFrame(
    confusion_matrix_, index=model.classes_, columns=model.classes_
)
classification_report_report_df.to_csv(os.path.join(output_dir, f"{testName}_confusion_matrix.csv"))

# Use output_dict=True for structured DataFrame
classification_report_dict = classification_report(y_test, y_pred, output_dict=True)
classification_report_df = pd.DataFrame(classification_report_dict).transpose()
classification_report_df.to_csv(os.path.join(output_dir, f"{testName}_classification_report.csv"))
