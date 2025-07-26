import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.header("Population of Canada")

df = pd.read_csv('quarterly_canada_population.csv')


with st.form("population_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Choose a start date")
        start_date_quarter = st.selectbox("Quarter", options=["Q1", "Q2", "Q3", "Q4"], index=2, key='start_date_quarter')
        start_date_year = st.slider("Year", min_value=1991, max_value=2023, value=1991, step=1, key='start_date_year')
    
    with col2:
        st.write("Choose an end date")
        end_date_quarter = st.selectbox("Quarter", options=["Q1", "Q2", "Q3", "Q4"], index=0, key='end_date_quarter')
        end_date_year = st.slider("Year", min_value=1991, max_value=2023, value=2023, step=1, key='end_date_year')

    with col3:
        st.write("Choose a location")
        location = st.selectbox("Choose a location", options=["Canada", "Alberta", "British Columbia", "Manitoba", "New Brunswick"], index=0, key='location')


    submit_button = st.form_submit_button("Submit", type="primary")


start_date = f"{start_date_quarter} {start_date_year}"
end_date = f"{end_date_quarter} {end_date_year}"


def get_date_index(df, date):
    return df[df["Quarter"] == date].index[0]


def compare_dates(start_date, end_date):
    start_index = get_date_index(df, start_date)
    end_index = get_date_index(df, end_date)
    if start_index > end_index:
        # st.error("Start date must be before end date")
        return False
    else:
        return True

def check_if_exists(date):
    if date not in df["Quarter"].tolist():
        # st.error(f"{date} does not exist in the dataset. Choose a different quarter for the year.")
        return False
    else:
        return True



def display_population_data(df, start_date, end_date, target):
    tab1, tab2 = st.tabs(["Population change", "Compare"])
    with tab1:
        st.subheader(f"Population Change From {start_date} to {end_date}")

        col1, col2 = st.columns(2)
        with col1:
            initial_value = df[df.Quarter == start_date][target].item()
            final_value = df[df.Quarter == end_date][target].item()
            # initial_value
            # final_value
            percent_change = round((final_value - initial_value) / initial_value * 100, 2)
            delta = f"{percent_change}%"
            st.metric(label=start_date, value=initial_value)
            st.metric(label = end_date, value=final_value, delta=delta)
        
        with col2:
            # We are filtering the data so that we only return the relevant data, not the whole dataframe
            filtered_df = df.iloc[get_date_index(df, start_date):get_date_index(df, end_date) + 1][["Quarter", target]]

            fig, ax = plt.subplots()
            ax.plot(filtered_df["Quarter"], filtered_df[target])
            ax.set_title(f"Population of {target} from {start_date} to {end_date}")
            ax.set_xlabel('Time')
            ax.set_xticks([start_date, end_date])
            ax.set_ylabel('Population')
            st.pyplot(fig)

            # st.dataframe(filtered_df, use_container_width=True)
    with tab2:
        st.subheader("Compare Population of Canada with other provinces")
        all_targets = st.multiselect("Choose other locations", options=df.columns[1:], default=[target], key='compare_locations')

        if len(all_targets) > 0:

            comparison_df = df[["Quarter"] + all_targets]
            # st.dataframe(comparison_df, use_container_width=True)

            fig, ax = plt.subplots()
            for col in all_targets:
                ax.plot(comparison_df["Quarter"], comparison_df[col], label=col)
            ax.set_title("Population Comparison")
            ax.set_xlabel('Time')
            ax.set_ylabel('Population')
            ax.set_xticks([start_date, end_date])
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("Please select at least one location to compare.")

if check_if_exists(start_date) == False:
    st.error(f"{start_date} does not exist in the dataset. Choose a different quarter for the year.")
elif check_if_exists(end_date) == False:
    st.error(f"{end_date} does not exist in the dataset. Choose a different quarter for the year.")
elif not compare_dates(start_date, end_date):
    st.error("Start date must be before end date")
else:
    display_population_data(df, start_date, end_date, location)
