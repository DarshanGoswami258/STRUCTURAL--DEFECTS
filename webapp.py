import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt
import os

#configure the model
key=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model=genai.GenerativeModel('gemini-2.5-flash-lite')


st.sidebar.title(':orange[UPLOAD YOUR IMAGE HERE]')
uploaded_image=st.sidebar.file_uploader('Here',type=['jpeg','jpg','png'])
if uploaded_image:
    image=Image.open(uploaded_image)
    st.sidebar.subheader(':blue[UPLOADED IMAGE]')
    st.sidebar.image(image)

# create main page
st.title('STRUCTURAL DEFECTS: :grey[AI assisted structural defect identifier in construction buisness]')
tips=''' to use the application follow the steps below:
* upload the image
* Click on the button to generate summary
* Click download to save the report generated'''
st.write(tips)
rep_title = st.text_input('Report Title :', None)
prep_by = st.text_input('Report Prepared By :', None)
prep_for = st.text_input('Report Prepared For :', None)


prompt='''Assume you are a structural engineer. The user has provided an image of a structure. you need
to identify the structural defects in the image and generate a report. the report should contain the follwoing:

It should with the title, prepared by and prepared for details. Provided by user. also use
{rep_title} as title, {prep_by} as prepared by, {prep_for} as prepared for the same.
also mention the current date from {dt.datetime.now().date()}.

* Identify and classify the defect for eg: crack, spalling, corrosion, honeycombing, etc
* There could more than one defect in the image. identify all the defects separately.
* for each defect identified, provide a short description of the defect and its potential impact on the structutre.
* for each measure the severity of the defect as low, medium or high. also mention if the defect is
* also mention the time before this defect leads to permanent damage to the structure.
* provide a short term and long term solutions along with thier estimated cost and time to impliment.
* what precautions measures can be taken to avoid such defects in future
* The report generated should be the word format.
* Show the data in bullet points and tabular format wherever possible.
* Make sure that the report should not exceed 3 pages.'''

if st.button('Generate Report'):
    if uploaded_image is None:
        st.error('Please upload an image first')
    else:
        with st.spinner('Generating Report...'):
            response=model.generate_content([prompt,image])
            st.write(response.text)
                
            st.download_button(
                label = 'Download Report',
                data = response.text,
                file_name = 'structural_defect_report.txt',
                mime = 'text/plain')

