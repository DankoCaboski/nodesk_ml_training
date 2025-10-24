import pandas as pd
import psycopg2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pickle
import os
from dotenv import load_dotenv

# === Carrega variáveis de ambiente ===
load_dotenv()

config = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS")
}

# === Conecta ao banco ===
conn = psycopg2.connect(**config)
table_name = os.getenv("TKT_RATED")

# === Lê os dados ===
df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
df.columns = df.columns.str.strip().str.lower()

# === Trata coluna de tempo ===
if "timetoresolve" in df.columns:
    df["timetoresolve"] = pd.to_timedelta(df["timetoresolve"]).dt.total_seconds() / 3600

# === Define features e target ===
features = ["totalinteractions", "slachangecount", "iscritical", "timetoresolve"]
X = df[features]
y = df["total_rating"]

# === Normaliza os dados ===
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === Divide treino/teste ===
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# === Treina o modelo ===
model = RandomForestClassifier(n_estimators=4, random_state=42)
model.fit(X_train, y_train)

# === Avaliação básica ===
y_pred = model.predict(X_test)
print("Matriz de confusão:\n", confusion_matrix(y_test, y_pred))
print("\nRelatório de classificação:\n", classification_report(y_test, y_pred))

# === Exporta modelo e scaler com pickle ===
os.makedirs("model", exist_ok=True)

with open("model/random_forest.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("model/scaler.pkl", "wb") as scaler_file:
    pickle.dump(scaler, scaler_file)

print("\n✅ Modelo e scaler salvos com sucesso na pasta 'model/'")
