import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
df=pd.DataFrame()
def main():
    st.title("Exploratory Data Analysis App")

    uploaded_file = st.file_uploader("Upload a CSV or XLSX file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        global df
        df = load_data(uploaded_file)

        st.subheader("Preview of the Data")
        st.write(df.head())

        if st.checkbox("Show Summary Statistics"):
            #st.write(df.describe())
            show_summary_statistics(df)

        if st.checkbox("Show NA Values Statistics"):
            na_stats = df.isna().sum()
            st.write("NA Values Statistics:")
            st.write(na_stats)

            handle_na_values(df)

        if st.checkbox("Show Data Visualization"):
            plot_data_hist(df)
        
        if st.checkbox("Convert Categorical Columns to One-Hot Encoded"):
            df_encoded = convert_to_one_hot(df)
            st.subheader("One-Hot Encoded Data")
            st.write(df_encoded.head())
            df = df_encoded
        if st.checkbox("Download Modified Data"):
            #modified_df = df  # Replace this with your actual data modification process

            # Allow user to select file location
            #save_as_csv(modified_df)
            export_file_name = st.text_input("Enter the name for the exported CSV file (without extension):")
            if export_file_name:
                # Save the modified DataFrame to the selected CSV file
                st.download_button(
               "Press to Download",
               convert_df(df),
               export_file_name+".csv",
               "text/csv",
               key='download-csv'
               )
            else:
                st.warning("Please enter a valid file name.")


@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
def convert_to_one_hot(df):
    st.subheader("Handling Categorical Columns")
    categorical_columns = df.select_dtypes(include=["object"]).columns

    for column in categorical_columns:
        st.write(f"Handling column: {column}")
        action = st.selectbox(f"Select action for column '{column}':", ["Skip", "Convert to One-Hot"])

        if action == "Skip":
            pass
        elif action == "Convert to One-Hot":
            df = pd.get_dummies(df, columns=[column], drop_first=True)

    st.write("Categorical columns handled according to your selections.")
    return df

    st.write("Categorical columns handled according to your selections.")
    return df
            
def show_summary_statistics(df):
    st.subheader("Summary Statistics")

    selected_column = st.selectbox("Select a column for summary statistics", df.columns)
    data_type = df[selected_column].dtype  # Get the data type of the selected column
    
    st.write(f"Data Type: {data_type}")
    st.write("Count of Unique Values:", df[selected_column].nunique())  # Count of unique values
    
    if data_type == "object":
        st.write("Object Type: Categorical")
    else:
        st.write("Object Type: Numerical")
        
    st.write(df[selected_column].describe())

def load_data(uploaded_file):
    if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    return df

def handle_na_values(df):
    st.subheader("Handling NA Values")

    columns_with_na = df.columns[df.isnull().any()]

    for column in columns_with_na:
        st.write(f"Handling NA values for column: {column}")
        if df[column].dtype == "object":
            # Handling categorical columns
            action = st.selectbox(f"Select action for column '{column}':", ["Drop NA Rows", "Fill with Mode", "Leave as NA"])
            
            if action == "Drop NA Rows":
                df = df.dropna(subset=[column])
            elif action == "Fill with Mode":
                mode_value = df[column].mode()[0]
                df[column].fillna(mode_value, inplace=True)
            elif action == "Leave as NA":
                pass
        else:
            # Handling numerical columns
            action = st.selectbox(f"Select action for column '{column}':", ["Drop NA Rows", "Fill with Mean", "Fill with Median", "Leave as NA"])
            
            if action == "Drop NA Rows":
                df = df.dropna(subset=[column])
            elif action == "Fill with Mean":
                df[column].fillna(df[column].mean(), inplace=True)
            elif action == "Fill with Median":
                df[column].fillna(df[column].median(), inplace=True)
            elif action == "Leave as NA":
                pass

    st.write("NA values handled according to your selections.")
    return df

def plot_data_hist(df):
    st.subheader("Data Visualization")
    fig, ax = plt.subplots()
    # Example: Create a histogram of a numerical column
    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns
    selected_column = st.selectbox("Select a numeric column for visualization", numeric_columns)
    #fig, ax = plt.subplots()
    ax.hist(df[selected_column], bins=20, edgecolor='k')
    plt.xlabel(selected_column)
    plt.ylabel("Frequency")
    st.pyplot(fig)

    # Option to plot chart with y-axis
    if st.checkbox("Plot Chart with Y-axis"):
        x_column = st.selectbox("Select X-axis column", df.columns, key="x_column_no_sum")
        y_column = st.selectbox("Select Y-axis column", numeric_columns, key="y_column_no_sum")
        
        fig, ax = plt.subplots()
        ax.plot(df[x_column], df[y_column], alpha=0.5)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)  # Use the selected Y-axis column as the label
        ax.set_title(f"{x_column} vs {y_column}")
        ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
        st.pyplot(fig)


    # Option to plot bar chart with sum as y-axis
    if st.checkbox("Plot Bar Chart with Sum as Y-axis"):
        x_column = st.selectbox("Select X-axis column", df.columns, key="x_column")
        y_column = st.selectbox("Select Y-axis column for sum", numeric_columns, key="y_column")
        
        summed_y = df.groupby(x_column)[y_column].sum()
        fig, ax = plt.subplots()
        ax.bar(summed_y.index, summed_y.values, alpha=0.5)
        plt.xlabel(x_column)
        plt.ylabel(f"Sum of {y_column}")
        plt.title(f"{x_column} vs Sum of {y_column}")
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        st.pyplot(fig)

    # Option to plot bar chart with top 10 highest sum values
    if st.checkbox("Plot Bar Chart with Top 10 Highest Sum Values"):
        x_column = st.selectbox("Select X-axis column", df.columns, key="x_column_top10")
        y_column = st.selectbox("Select Y-axis column for sum", numeric_columns, key="y_column_top10")
        
        summed_y = df.groupby(x_column)[y_column].sum()
        top_10_summed_y = summed_y.nlargest(10)  # Select top 10 highest sum values
        fig, ax = plt.subplots()
        ax.bar(top_10_summed_y.index, top_10_summed_y.values, alpha=0.5)
        plt.xlabel(x_column)
        plt.ylabel(f"Sum of {y_column}")
        plt.title(f"Top 10 {x_column} vs Sum of {y_column}")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        # Option to plot bar chart with top 10 highest sum values
    if st.checkbox("Plot Bar Chart with Top 10 Lowest Sum Values"):
        x_column = st.selectbox("Select X-axis column", df.columns, key="x_column_low10")
        y_column = st.selectbox("Select Y-axis column for sum", numeric_columns, key="y_column_low10")
        
        summed_y = df.groupby(x_column)[y_column].sum()
        low_10_summed_y = summed_y.nsmallest(10)  # Select top 10 highest sum values
        fig, ax = plt.subplots()
        ax.bar(top_10_summed_y.index, low_10_summed_y.values, alpha=0.5)
        plt.xlabel(x_column)
        plt.ylabel(f"Sum of {y_column}")
        plt.title(f"Top 10 {x_column} vs Sum of {y_column}")
        plt.xticks(rotation=45)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
