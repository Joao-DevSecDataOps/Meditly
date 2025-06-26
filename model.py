import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
import joblib
import database

MODEL_PATH = "cbt_distortion_model.joblib"

def train_and_save_model():
    print("Iniciando o treinamento do modelo...")
    training_data = database.get_data_for_ml_training()
    if len(training_data) < 10:
        print(f"AVISO: Dados insuficientes para treinamento ({len(training_data)} registros). O modelo não será treinado.")
        return
    df = pd.DataFrame(training_data, columns=['pensamento', 'distorcoes'])
    X_train = df['pensamento']
    y_train_labels = df['distorcoes']
    print(f"{len(df)} registros de treinamento encontrados.")
    mlb = MultiLabelBinarizer()
    y_train_binarized = mlb.fit_transform(y_train_labels)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words=None, ngram_range=(1, 2), max_features=2000)),
        ('clf', OneVsRestClassifier(LogisticRegression(solver='liblinear', class_weight='balanced'), n_jobs=-1))
    ])
    print("Treinando o pipeline...")
    pipeline.fit(X_train, y_train_binarized)
    model_bundle = {'pipeline': pipeline, 'binarizer': mlb}
    joblib.dump(model_bundle, MODEL_PATH)
    print(f"Modelo treinado e salvo com sucesso em '{MODEL_PATH}'!")
    print(f"Classes (distorções) que o modelo aprendeu: {list(mlb.classes_)}")

if __name__ == '__main__':
    train_and_save_model()