import streamlit as st
import pandas as pd
import joblib

# Load pre-trained pipeline and column names
inputs = joblib.load("columns_names.pkl")
pipeline = joblib.load("pipeline.pkl")
user_cuisine = joblib.load("cuisines_input.pkl")
cuisines_columns = joblib.load("cuisines_columns.pkl")
user_rest = joblib.load("rest_type_input.pkl")
location_unique = joblib.load("location_unique.pkl")
city_unique = joblib.load("city_unique.pkl")
type_unique = joblib.load("type_unique.pkl")

# Streamlit app header and images
st.header("Zomato Restaurant Classifier")


def main():
    global location_unique, city_unique, type_unique, user_rest, user_cuisine, cuisines_columns, pipeline
    
    try:
        online_order = st.selectbox("Are online orders available?", ["Yes", "No"])
        book_table = st.selectbox("Is Booking a table available?", ["Yes", "No"])
        location = st.selectbox("Your Restaurant Location", location_unique)
        city = st.selectbox("Your Restaurant City", city_unique)
        rest_type = st.selectbox("Which of these categories is your restaurant?", type_unique)
        approx_cost = st.slider("Approximate cost for 2 people", min_value=35.0, max_value=6000.0, value=682.0, step=10.0)
        
        rest_types_selected = st.multiselect("Which Rest type does your restaurant fit into?", user_rest)
        cuisines_selected = st.multiselect("Cuisines included in your restaurant", user_cuisine)



        data = {col: 0 for col in inputs}

        data["online_order"] = 1 if online_order == "Yes" else 0
        data["book_table"] = 1 if book_table == "Yes" else 0
        data["location"] = location  
        data["approx_cost_for_2_people"] = approx_cost
        data["listed_in_type"] = rest_type
        data["listed_in_city"] = city
    
        for rest in user_rest:  
            if rest in rest_types_selected:  
                data[rest] = 1  
            else:
                data[rest] = 0  
        
        for cuisine in user_cuisine:
            if cuisine in cuisines_selected:  
                data[cuisine + "_cuisine"] = 1 
            else:
                data[cuisine + "_cuisine"] = 0  

        df = pd.DataFrame([data])
        
        result = pipeline.predict(df)
        
        if st.button("Predict"): 
            if len(rest_types_selected) == 0:
                st.error("Please select at least one restaurant type.")
                return  # Stop the function from proceeding

            if len(cuisines_selected) == 0:
                st.error("Please select at least one cuisine.")
                return  # Stop the function from proceeding 
               
            if result[0] == 1:
                st.text("Probably Your Restaurant will Succeed :)")
                st.image("right sign.jpg" , width=200 )

            else:
                st.text("Probably Your Restaurant will Fail :(")
                st.image("sad.jpeg" , width=200 )

                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}. Please check your inputs and try again.")

# Run the prediction function
main()
