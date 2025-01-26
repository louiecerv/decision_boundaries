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
    st.title("📊📈Visualizing Decision Boundaries in Machine Learning Algorithms🧮")

    about = """
This interactive application provides a platform for computer science students to gain a deeper understanding of how various machine learning algorithms approach classification tasks. By manipulating data characteristics and observing the resulting decision boundaries, students can develop an intuitive grasp of the strengths and weaknesses of different models.

**Key Features:**

* **Configurable Data Generation:**  Fine-grained control over the number of clusters, sample size, and standard deviation allows for the creation of diverse datasets, including those with complex overlapping clusters. This facilitates the exploration of model performance under varying degrees of data separability.
* **Comparative Model Visualization:**  Observe and analyze the decision boundaries generated by a range of machine learning algorithms, including Support Vector Machines (SVMs), k-Nearest Neighbors (k-NN), and Decision Trees.  Directly compare the efficacy of different approaches in classifying data with varying levels of complexity.
* **Interactive Exploration:** Experiment with different parameter settings and observe the impact on the generated decision boundaries. This hands-on approach fosters active learning and reinforces theoretical concepts.

**Learning Objectives:**

* Develop a visual understanding of decision boundaries in machine learning.
* Gain insights into the influence of data characteristics on model performance.
* Compare and contrast the classification strategies of different algorithms.
* Analyze the effectiveness of various models in handling overlapping clusters.
* Enhance understanding of bias-variance tradeoffs and model complexity.

**This application is an invaluable tool for:**

* **Illustrating core machine learning concepts:**  Provides a concrete visualization of abstract theoretical principles.
* **Reinforcing classroom learning:** Complements lectures and textbook material with interactive experimentation.
* **Encouraging independent exploration:**  Empowers students to investigate the behavior of machine learning algorithms autonomously.

**💡Created by: Louie F. Cervantes, M. Eng. (Information Engineering)**
(c) 2025 West Visayas State University
    """
    with st.expander("About this app"):
        st.markdown(about)
    
    with st.sidebar:
        st.header("Data Parameters")
        n_samples = st.slider("Number of Samples", 300, 1000, 500)
        cluster_std = st.slider("Cluster Standard Deviation", 0.1, 3.0, 0.5)
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
            
    st. write("© 2025 West Visayas State University")
if __name__ == "__main__":
    main()
