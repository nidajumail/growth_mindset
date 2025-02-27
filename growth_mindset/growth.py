import streamlit as st
import pandas as pd 
import os
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout="wide")

#use custom css
st.markdown(
    """"
    <style>
    .stApp{
    background-color: #f0f0f5;
    color:white;}
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Data Sweeper sterling intergrator by Nida Haq")
st.write("Transform your files between CSV to Excel formats with built-in data cleaning and visualization Creating the project for quarter 3!")

#file upload
uploaded_file = st.file_uploader("Upload your files (accepts CSV and Excel):", type=["csv","xlsx"], accept_multiple_files=(True))

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type {file_ext}")
            continue
        
     
        st.write("🔍 Preview the head of the dataframe")
        st.dataframe(df.head())


# data cleaning
st.subheader(" Data Cleaning Options")
if st.checkbox(f"Clean data for {file.name}"):
    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"Remove duplicates from the file: {file.name}"):
            df.drop_duplicates(inplace=True)
            st.write("✅ Duplicates removed!")

    with col2:
        if st.button(f"Fill missing Values for {file.name}"):
            numeric_cols = df.select_dtypes(include=["number"]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df.mean())
            st.write("✅ Missing values has been filled!")

            st.subheader(" Select column to keep ")
            column=st.multiselect(f"Select the columns {file.name}", df.columns,default=df.columns)
            df=df[column]

            #data visualization
            st.subheader(" 📊Data Visualization")
            if st.checkbox(f"📊 Show visualization for {file.name}"):
             st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
        

        #Conversion Options
        st.subheader(" Conversion Options")
        conversion_type = st.radio(f"Convert{file.name} to:", ["CSV", "Excel"])
        if st.button(f"Convert {file.name}"):
           buffer = BytesIO()
        if conversion_type == "CSV":
                   df.to_csv(buffer, index=False)
                   file_name = file.name.replace(file_ext,".csv")
                   mime_type = "text/csv"
                                
        elif conversion_type == "Excel":
                   df.to_excel(buffer, index=False)
                   file_name = file.name.replace(file_ext, ".xlsx")
                   mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)

st.download_button(
        label=f"Click to download {file_name} as {conversion_type}", 
        data=buffer,
         file_name=file_name,
          mime=mime_type)


st.success("All files proccessed successfully!")

 
