import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report

def generate_random_points_in_square(x_min, x_max, y_min, y_max, n_clusters):
    np.random.seed(42)
    return np.random.uniform(low=[x_min, y_min], high=[x_max, y_max], size=(n_clusters, 2))

def generate_data(n_samples, cluster_std, random_state, n_clusters):
    centers = generate_random_points_in_square(-4, 4, -4, 4, n_clusters)
    X, y = make_blobs(n_samples=n_samples, n_features=2, cluster_std=cluster_std, 
                       centers=centers, random_state=random_state)
    return X, y

def train_and_evaluate_model(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred)
    return model, cm, cr

def visualize_classifier(classifier, X, y, title=''):
    min_x, max_x = X[:, 0].min() - 1.0, X[:, 0].max() + 1.0
    min_y, max_y = X[:, 1].min() - 1.0, X[:, 1].max() + 1.0
    mesh_step_size = 0.01
    x_vals, y_vals = np.meshgrid(np.arange(min_x, max_x, mesh_step_size), 
                                  np.arange(min_y, max_y, mesh_step_size))
    output = classifier.predict(np.c_[x_vals.ravel(), y_vals.ravel()])
    output = output.reshape(x_vals.shape)
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.pcolormesh(x_vals, y_vals, output, cmap=plt.cm.gray)
    ax.scatter(X[:, 0], X[:, 1], c=y, s=75, edgecolors='black', linewidth=1, cmap=plt.cm.Paired)
    ax.set_xlim(x_vals.min(), x_vals.max())
    ax.set_ylim(y_vals.min(), y_vals.max())
    ax.set_xticks(np.arange(int(X[:, 0].min() - 1), int(X[:, 0].max() + 1), 1.0))
    ax.set_yticks(np.arange(int(X[:, 1].min() - 1), int(X[:, 1].max() + 1), 1.0))
    st.pyplot(fig)

def main():
    st.title("Machine Learning Model Comparison")
    with st.sidebar:
        st.header("Data Parameters")
        n_samples = st.slider("Number of Samples", 300, 1000, 500)
        cluster_std = st.slider("Cluster Standard Deviation", 0.1, 1.0, 0.5)
        random_state = st.slider("Random State", 0, 100, 42)
        n_clusters = st.slider("Number of Clusters", 2, 6, 2)
    
    with st.spinner("Generating data and training models..."):
        X, y = generate_data(n_samples, cluster_std, random_state, n_clusters)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        models = {
            "Logistic Regression": LogisticRegression(),
            "Naive Bayes": GaussianNB(),
            "SVM": SVC(),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier(),
            "KNN": KNeighborsClassifier()
        }
        results = {}
        trained_models = {}
        for name, model in models.items():
            trained_model, cm, cr = train_and_evaluate_model(model, X_train, X_test, y_train, y_test)
            results[name] = (trained_model, cm, cr)
    
    tabs = st.tabs(models.keys())
    for tab, (name, (trained_model, cm, cr)) in zip(tabs, results.items()):
        with tab:
            st.subheader(name)
            fig, ax = plt.subplots()
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
            ax.set_xlabel("Predicted Labels")
            ax.set_ylabel("True Labels")
            ax.set_title("Confusion Matrix")
            st.pyplot(fig)
            st.text("Classification Report")
            st.write(cr)
            visualize_classifier(trained_model, X_train, y_train, title=f"{name} Decision Boundary")

if __name__ == "__main__":
    main()
