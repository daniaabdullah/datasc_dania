import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title='Analyze Your Data', page_icon='📊', layout='wide')
st.title("📊 Analyze Your Data")
st.write("Upload A **CSV** Or An **Excel** File To Explore Data Interactively!")

# 1. Handling File Upload for both CSV and Excel
uploaded_file = st.file_uploader("Upload A CSV Or An Excel File", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Determine which function to use based on file extension
        if uploaded_file.name.endswith('.csv'):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        # Converting boolean data types to strings for better display
        bool_cols = data.select_dtypes(include=['bool']).columns
        data[bool_cols] = data[bool_cols].astype('str')
        
    except Exception as e:
        st.error("Could Not Read File. Please Check The File Format")
        st.exception(e)
        st.stop()

    st.success(f'✅ {uploaded_file.name} Uploaded Successfully ✅')
    
    # 2. Data Overview Section
    st.write("### Preview of Data")
    st.dataframe(data.head())

    st.write("### Data Overview")
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Rows", data.shape[0])
    col_b.metric("Columns", data.shape[1])
    col_c.metric("Missing Values", data.isnull().sum().sum())
    col_d.metric("Duplicates", data.duplicated().sum())

    # 3. Summary Statistics
    st.write("### Complete Summary of Dataset")
    buffer = io.StringIO()
    data.info(buf=buffer)
    st.text(buffer.getvalue())
    
    st.write("### 📊 Statistical Summary (Numerical)")
    st.dataframe(data.describe())

    # 4. Conditional Check for Non-Numerical Features
    # This must be INDENTED to stay inside the "if uploaded_file" block
    non_num_data = data.select_dtypes(include=["object", "string"])

    if not non_num_data.empty:
        st.write("### 📊 Statistical Summary (Non-Numerical)")
        # Convert to string to fix the Arrow serialization error from earlier
        st.dataframe(non_num_data.astype(str).describe())
    else:
        st.info("ℹ️ No non-numerical features found for a summary.")

    # 5. Column Selection
    st.write("### 📌 Select Columns For Analysis")
    selected_columns = st.multiselect('Choose Columns', data.columns.tolist())

    if selected_columns:
        st.dataframe(data[selected_columns].head())
    else:
        st.info("Showing Full Dataset Preview")
        st.dataframe(data.head())

    # 6. Data Visualization
    st.write("### 📈 Data Visualization")
    columns = data.columns.tolist()
    
    x_axis = st.selectbox("Select Column For X-Axis", options=columns)
    y_axis = st.selectbox("Select Column For Y-Axis", options=columns)

    col1, col2, col3 = st.columns(3)
    line_btn = col1.button("Generate Line Graph")
    scatter_btn = col2.button("Generate Scatter Plot")
    bar_btn = col3.button("Generate Bar Graph")

    # Visualization Logic
    if line_btn or scatter_btn or bar_btn:
        fig, ax = plt.subplots()
        
        if line_btn:
            st.write("### Line Graph")
            ax.plot(data[x_axis], data[y_axis])
        elif scatter_btn:
            st.write("### Scatter Plot")
            ax.scatter(data[x_axis], data[y_axis])
        elif bar_btn:
            st.write("### Bar Graph")
            ax.bar(data[x_axis], data[y_axis])
            
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"{x_axis} vs {y_axis}")
        st.pyplot(fig)



