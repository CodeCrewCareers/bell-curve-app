import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Title
st.title("Bell Curve Grading Tool")

# File upload
uploaded_file = st.file_uploader("Upload your file (CSV)", type=["csv"])


if uploaded_file:
    # Load the file into a DataFrame
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:")
    st.write(data.head())

    # Dropdown to select the score column
    score_column = st.selectbox("Select the column with scores:", data.columns)

    if score_column:
        scores = data[score_column]
        
        # Calculate mean and standard deviation
        mean = np.mean(scores)
        std = np.std(scores)
        
        # Normalize the scores (bell curve standardization)
        z_scores = (scores - mean) / std
        
        # Calculate grades
        grading_scale = {
            "A": lambda z: z >= 1.0,
            "B": lambda z: 0.0 <= z < 1.0,
            "C": lambda z: -1.0 <= z < 0.0,
            "D": lambda z: -2.0 <= z < -1.0,
            "F": lambda z: z < -2.0
        }
        
        def assign_grade(z):
            for grade, condition in grading_scale.items():
                if condition(z):
                    return grade
            return "F"

        data["Z-Score"] = z_scores
        data["Grade"] = data["Z-Score"].apply(assign_grade)
        
        # Display data with grades
        st.write("Data with Grading:")
        st.write(data)

        # Plot the bell curve
        x = np.linspace(mean - 3 * std, mean + 3 * std, 1000)
        y = norm.pdf(x, mean, std)

        plt.figure(figsize=(10, 6))
        plt.hist(scores, bins=20, density=True, alpha=0.6, color='gray', label='Histogram of Scores')
        plt.plot(x, y, label='Normal Distribution', color='red')
        plt.axvline(mean, color='blue', linestyle='--', label='Mean')
        plt.title("Bell Curve of Scores")
        plt.xlabel("Scores")
        plt.ylabel("Density")
        plt.legend()
        st.pyplot(plt)

        # Option to download results
        csv_data = data.to_csv(index=False).encode('utf-8')
        st.download_button("Download Graded Data", csv_data, "graded_data.csv", "text/csv")
