import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


st.title("NSW HSC result explorer")

DATA = Path(__file__).resolve().parent.parent / "data" / "processed"/ "hsc_bands_clean.csv"

#cache the data
@st.cache_data
def load_data():
    df = pd.read_csv(DATA)
    band_order = ["1","2","3","4","5","6","E1","E2","E3","E4"]
    df["band"] = pd.Categorical(df["band"],categories=band_order,ordered=True)
    return df

df = load_data()

#FILTER

subjects = sorted(df["course_name"].unique())
subject = st.sidebar.selectbox("Subject", subjects)

sub = df[df["course_name"] == subject]

st.subheader(subject)
st.dataframe(sub)

pivot = sub.pivot(index="year",columns="band", values="percentage").dropna(axis=1, how = "all") #drop empty E-band columns

fig, ax = plt.subplots()
pivot.plot(ax=ax, marker="o")
ax.set_ylabel("% of students")
ax.set_title(f"{subject}: band distribution 2021-2025")

# CANDIDATURE
enrol = sub.groupby("year")["candidature"].first()

fig2, ax2 = plt.subplots()
enrol.plot(ax=ax2, marker = "o")
ax2.set_ylabel("Number of students")
ax2.set_title(f"{subject}: enrolment 2021-2025")

#Put 2 charts in 1 column
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig) #BAND
with col2:
    st.pyplot(fig2) #enrolment


#Cros-subject overview
st.header("How subjects compare — top-band rate")

top = df[df["band"].isin(["6", "E4"])]
top_by_subject = top.groupby("course_name")["percentage"].mean().sort_values()

fig3, ax3 = plt.subplots()
colors = ["tomato" if name == subject else "steelblue" for name in top_by_subject.index]
top_by_subject.plot(kind="barh", ax=ax3, color=colors)         
ax3.set_xlabel("Mean % in top band (Band 6 / E4), 2021–2025")
ax3.set_title("Top-band rate by subject")
st.pyplot(fig3)