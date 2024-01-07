import os
import json
import pandas as pd
import mysql.connector
import streamlit as st
import requests
import plotly
import plotly.express as px
import plotly.graph_objects as go

mysql_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="3127",
    database="Phonepe_Data",
    port="3306"
)

cursor = mysql_connection.cursor()

# Aggregated_transsaction
cursor.execute("SELECT * FROM aggregated_transaction;")
table1 = cursor.fetchall()
Aggre_trans = pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

# Aggregated_user
cursor.execute("SELECT * FROM aggregated_user")
table2 = cursor.fetchall()
Aggre_user = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

# Map_transaction
cursor.execute("SELECT * FROM map_transaction")
table3 = cursor.fetchall()
Map_trans = pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

# Map_user
cursor.execute("SELECT * FROM map_user")
table4 = cursor.fetchall()
Map_user = pd.DataFrame(table4, columns=("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

# Top_transaction
cursor.execute("SELECT * FROM top_transaction")
table5 = cursor.fetchall()
Top_trans = pd.DataFrame(table5, columns=("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

# Top_user
cursor.execute("SELECT * FROM top_user")
table6 = cursor.fetchall()
Top_user = pd.DataFrame(table6, columns=("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))

cursor.close()
mysql_connection.close()


def animate_all_amount():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    state_names_tra = [feature["properties"]["ST_NM"] for feature in data1["features"]]
    state_names_tra.sort()

    df_state_names_tra = pd.DataFrame({"States": state_names_tra})

    frames = []

    for year in Map_user["Years"].unique():
        for quarter in Aggre_trans["Quarter"].unique():
            at1 = Aggre_trans[(Aggre_trans["Years"] == year) & (Aggre_trans["Quarter"] == quarter)]
            atf1 = at1[["States", "Transaction_amount"]]
            atf1 = atf1.sort_values(by="States")
            atf1["Years"] = year
            atf1["Quarter"] = quarter
            frames.append(atf1)

    merged_df = pd.concat(frames)

    fig_tra = px.choropleth(merged_df, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                            color="Transaction_amount",
                            color_continuous_scale="Sunsetdark", range_color=(0, 4000000000), hover_name="States",
                            title="TRANSACTION AMOUNT",
                            animation_frame="Years", animation_group="Quarter")

    fig_tra.update_geos(fitbounds="locations", visible=False)
    fig_tra.update_layout(width=600, height=700)
    fig_tra.update_layout(title_font={"size": 25})
    return st.plotly_chart(fig_tra)


def payment_count():
    attype = Aggre_trans[["Transaction_type", "Transaction_count"]]
    att1 = attype.groupby("Transaction_type")["Transaction_count"].sum()
    df_att1 = pd.DataFrame(att1).reset_index()
    fig_pc = px.bar(df_att1, x="Transaction_type", y="Transaction_count",
                    title="TRANSACTION TYPE and TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Redor_r)
    fig_pc.update_layout(width=600, height=500)
    return st.plotly_chart(fig_pc)


def animate_all_count():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    state_names_tra = [feature["properties"]["ST_NM"] for feature in data1["features"]]
    state_names_tra.sort()

    df_state_names_tra = pd.DataFrame({"States": state_names_tra})

    frames = []

    for year in Aggre_trans["Years"].unique():
        for quarter in Aggre_trans["Quarter"].unique():
            at1 = Aggre_trans[(Aggre_trans["Years"] == year) & (Aggre_trans["Quarter"] == quarter)]
            atf1 = at1[["States", "Transaction_count"]]
            atf1 = atf1.sort_values(by="States")
            atf1["Years"] = year
            atf1["Quarter"] = quarter
            frames.append(atf1)

    merged_df = pd.concat(frames)

    fig_tra = px.choropleth(merged_df, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                            color="Transaction_count", color_continuous_scale="Sunsetdark", range_color=(0, 3000000),
                            title="TRANSACTION COUNT", hover_name="States", animation_frame="Years",
                            animation_group="Quarter")

    fig_tra.update_geos(fitbounds="locations", visible=False)
    fig_tra.update_layout(width=600, height=700)
    fig_tra.update_layout(title_font={"size": 25})
    return st.plotly_chart(fig_tra)


def payment_amount():
    attype = Aggre_trans[["Transaction_type", "Transaction_amount"]]
    att1 = attype.groupby("Transaction_type")["Transaction_amount"].sum()
    df_att1 = pd.DataFrame(att1).reset_index()
    fig_tra_pa = px.bar(df_att1, x="Transaction_type", y="Transaction_amount",
                        title="TRANSACTION TYPE and TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Viridis)
    fig_tra_pa.update_layout(width=600, height=500)
    return st.plotly_chart(fig_tra_pa)


def reg_all_states(state):
    state_names = Map_user["States"].unique()
    state_names.sort()

    df_state_names = pd.DataFrame({"States": state_names})

    for quarter in Aggre_user["Quarter"].unique():
        au1 = Aggre_user[(Aggre_user["Quarter"] == quarter)]
        auf1 = au1[["States", "Transaction_count"]]
        auf1 = auf1.sort_values(by="States")

        fig_regs = px.bar(auf1, x="States", y="Transaction_count", title="REGISTERED USERS", color_discrete_sequence=px.colors.sequential.Purpor)
        fig_regs.update_layout(width=1200, height=600)
        st.plotly_chart(fig_regs)


def transaction_amount_year(sel_year):
    at1 = Aggre_trans[(Aggre_trans["Years"] == sel_year)]
    atf1 = at1[["States", "Transaction_amount"]]
    atf1 = atf1.sort_values(by="States")
    fig_tra_year = px.bar(atf1, x="States", y="Transaction_amount", title="TRANSACTION AMOUNT YEAR WISE",
                          color_discrete_sequence=px.colors.sequential.Magenta)
    fig_tra_year.update_layout(width=1200, height=600)
    return st.plotly_chart(fig_tra_year)


def payment_count_year(sel_year):
    at1 = Aggre_trans[(Aggre_trans["Years"] == sel_year)]
    atf1 = at1[["States", "Transaction_count"]]
    atf1 = atf1.sort_values(by="States")
    fig_pc_year = px.bar(atf1, x="States", y="Transaction_count", title="TRANSACTION COUNT YEAR WISE",
                         color_discrete_sequence=px.colors.sequential.Inferno)
    fig_pc_year.update_layout(width=1200, height=600)
    return st.plotly_chart(fig_pc_year)


def transaction_count_year(sel_year):
    at1 = Aggre_trans[(Aggre_trans["Years"] == sel_year)]
    atf1 = at1[["States", "Transaction_count"]]
    atf1 = atf1.sort_values(by="States")
    fig_tc_year = px.bar(atf1, x="States", y="Transaction_count", title="TRANSACTION COUNT YEAR WISE",
                         color_discrete_sequence=px.colors.sequential.Plasma)
    fig_tc_year.update_layout(width=1200, height=600)
    return st.plotly_chart(fig_tc_year)


def payment_amount_year(sel_year):
    at1 = Aggre_trans[(Aggre_trans["Years"] == sel_year)]
    atf1 = at1[["States", "Transaction_amount"]]
    atf1 = atf1.sort_values(by="States")
    fig_pa_year = px.bar(atf1, x="States", y="Transaction_amount", title="TRANSACTION AMOUNT YEAR WISE",
                         color_discrete_sequence=px.colors.sequential.Sunsetdark)
    fig_pa_year.update_layout(width=1200, height=600)
    return st.plotly_chart(fig_pa_year)





def reg_state_all_RU(sel_year, state):
    mu = Map_user[["States", "Districts", "RegisteredUser"]]
    mu1 = mu.loc[(mu["States"] == state)]
    mu2 = mu1[["Districts", "RegisteredUser"]]
    mu3 = mu2.groupby("Districts")["RegisteredUser"].sum()
    mu4 = pd.DataFrame(mu3).reset_index()
    fig_mu = px.bar(mu4, x="Districts", y="RegisteredUser", title="DISTRICTS and REGISTERED USER",
                   color_discrete_sequence=px.colors.sequential.Bluered_r)
    fig_mu.update_layout(width=1000, height=500)
    return st.plotly_chart(fig_mu)

def reg_state_all_TA(sel_year, state):
    au1 = Aggre_user[(Aggre_user["Years"] == sel_year) & (Aggre_user["States"] == state)]
    auf1 = au1[["Quarter", "Transaction_count"]]
    auf1 = auf1.sort_values(by="Quarter")
    fig_regs_TA = px.bar(auf1, x="Quarter", y="Transaction_count", title=f"TRANSACTION AMOUNT IN {state}",
                        color_discrete_sequence=px.colors.sequential.Plasma)
    fig_regs_TA.update_layout(width=600, height=500)
    st.plotly_chart(fig_regs_TA)


def ques1():
    fig_ques1 = px.bar(Top_trans, x="States", y="Transaction_count", title="Q1: TOP 5 STATES IN TRANSACTION COUNT",
                      color_discrete_sequence=px.colors.sequential.Viridis)
    fig_ques1.update_layout(width=1200, height=600)
    return st.plotly_chart(fig_ques1)


def ques2():
    fig_ques2 = px.bar(Top_trans, x="States", y="Transaction_amount", title="Q2: TOP 5 STATES IN TRANSACTION AMOUNT",
                      color_discrete_sequence=px.colors.sequential.Sunsetdark)
    fig_ques2.update_layout(width=1200, height=600)
    return st.plotly_chart(fig_ques2)


def ques3():
    fig_ques3 = px.bar(Top_user, x="States", y="RegisteredUser", title="Q3: TOP 5 STATES IN REGISTERED USERS",
                      color_discrete_sequence=px.colors.sequential.Plasma)
    fig_ques3.update_layout(width=1200, height=600)
    return st.plotly_chart(fig_ques3)


def ques4():
    htd = Map_trans[["Districts", "Transaction_amount"]]
    htd1 = htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2 = pd.DataFrame(htd1).head(10).reset_index()

    fig_htd = px.pie(htd2, values="Transaction_amount", names="Districts",
                     title="Q4: TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                     color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    state_names_tra = [feature["properties"]["ST_NM"] for feature in data1["features"]]
    state_names_tra.sort()

    df_state_names_tra = pd.DataFrame({"States": state_names_tra})

    frames = []

    for year in Map_user["Years"].unique():
        for quarter in Aggre_trans["Quarter"].unique():
            at1 = Aggre_trans[(Aggre_trans["Years"] == year) & (Aggre_trans["Quarter"] == quarter)]
            atf1 = at1[["States", "Transaction_amount"]]
            atf1 = atf1.sort_values(by="States")
            atf1["Years"] = year
            atf1["Quarter"] = quarter
            frames.append(atf1)

    merged_df = pd.concat(frames)

    fig_ques5 = px.choropleth(merged_df, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                              color="Transaction_amount", color_continuous_scale="Sunsetdark", range_color=(0, 4000000000),
                              title="Q5: ANIMATION - TRANSACTION AMOUNT",
                              animation_frame="Years", animation_group="Quarter")

    fig_ques5.update_geos(fitbounds="locations", visible=False)
    fig_ques5.update_layout(width=600, height=700)
    fig_ques5.update_layout(title_font={"size": 25})
    return st.plotly_chart(fig_ques5)


def ques6():
    fig_ques6 = px.bar(Aggre_trans, x="Transaction_type", y="Transaction_amount",
                      title="Q6: TRANSACTION AMOUNT BASED ON TRANSACTION TYPE",
                      color_discrete_sequence=px.colors.sequential.Magma)
    fig_ques6.update_layout(width=1200, height=600)
    return st.plotly_chart(fig_ques6)


def ques7():
    fig_ques7 = px.bar(Aggre_user, x="Brands", y="Transaction_count", title="Q7: TRANSACTION COUNT BASED ON BRANDS",
                      color_discrete_sequence=px.colors.sequential.Sunsetdark)
    fig_ques7.update_layout(width=1200, height=600)
    return st.plotly_chart(fig_ques7)


def ques8():
    fig_ques8 = px.bar(Map_trans, x="Districts", y="Transaction_amount",
                      title="Q8: TRANSACTION AMOUNT BASED ON DISTRICTS",
                      color_discrete_sequence=px.colors.sequential.Magenta)
    fig_ques8.update_layout(width=1200, height=600)
    return st.plotly_chart(fig_ques8)


def ques9():
    fig_ques9 = px.bar(Map_user, x="Districts", y="RegisteredUser",
                      title="Q9: REGISTERED USERS BASED ON DISTRICTS",
                      color_discrete_sequence=px.colors.sequential.Purples)
    fig_ques9.update_layout(width=1200, height=600)
    return st.plotly_chart(fig_ques9)


def ques10():
    fig_ques10 = px.bar(Top_user, x="Pincodes", y="RegisteredUser", title="Q10: REGISTERED USERS BASED ON PINCODES",
                       color_discrete_sequence=px.colors.sequential.Plasma)
    fig_ques10.update_layout(width=1200, height=600)
    return st.plotly_chart(fig_ques10)


st.set_page_config(layout="wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
tab1, tab2, tab3 = st.tabs(["***HOME***", "***EXPLORE DATA***", "***TOP CHARTS***"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("   **-> Credit & Debit card linking**")
        st.write("   **-> Bank Balance check**")
        st.write("   **->Money Storage**")
        st.write("   **->PIN Authorization**")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

    with col2:
        st.write("**-> Easy Transactions**")
        st.write("**-> One App For All Your Payments**")
        st.write("**-> Your Bank Account Is All You Need**")
        st.write("**-> Multiple Payment Modes**")
        st.write("**-> PhonePe Merchants**")
        st.write("**-> Multiple Ways To Pay**")
        st.write("**-> 1.Direct Transfer & More**")
        st.write("**-> 2.QR Code**")
        st.write("**-> Earn Great Rewards**")

    col3, col4 = st.columns(2)

    with col3:
        pass  # No video included

    with col4:
        pass  # No video included

    col5, col6 = st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("**->No Wallet Top-Up Required**")
        st.write("**->Pay Directly From Any Bank To Any Bank A/C**")
        st.write("**->Instantly & Free**")

    with col6:
        pass  # No video included

with tab2:
    sel_year = st.selectbox("select the Year",("All", "2018", "2019", "2020", "2021", "2022", "2023"))
    if sel_year == "All" :
        col1, col2 = st.columns(2)
        with col1:
            animate_all_amount()
            payment_count()
            
        with col2:
            animate_all_count()
            payment_amount()

        state=st.selectbox("selecet the state",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                'Uttarakhand', 'West Bengal'))
        reg_all_states(state)

    else:
        col1,col2= st.columns(2)

        with col1:
            transaction_amount_year(sel_year)
            payment_count_year(sel_year)

        with col2:
            transaction_count_year(sel_year)
            payment_amount_year(sel_year)
            state= st.selectbox("selecet the state",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                'Uttarakhand', 'West Bengal'))
            reg_state_all_RU(sel_year,state)
            reg_state_all_TA(sel_year,state)

with tab3:
    ques= st.selectbox("select the question",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()
