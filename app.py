import pandas as pd
import numpy as np
import streamlit as st
import scipy.stats as ss
import altair as alt
import webbrowser


st.set_page_config(page_title="Scipy Stats Distribution Zoo", layout="wide")


@st.cache
def get_continuous_dist():
    return sorted(ss._continuous_distns._distn_names)


@st.cache
def get_discrete_dist():
    return sorted(ss._discrete_distns._distn_names)


@st.cache
def get_dist(distribution):
    return getattr(ss, dist_name)


@st.cache
def ls_params(distribution):
    if distribution.shapes:
        p = [name.strip() for name in distribution.shapes.split(",")]
    else:
        p = []
    if distribution.name in discrete_dists:
        p += ["loc"]
    elif distribution.name in continuous_dists:
        p += ["loc", "scale"]
    return p


continuous_dists = get_continuous_dist()
discrete_dists = get_discrete_dist()


st.sidebar.write("## Select distribution")
dist_cat = st.sidebar.radio("", ["continuous", "discrete"])

param_val_default = dict(loc=0, scale=1)

if dist_cat == "continuous":
    dist_list = continuous_dists
elif dist_cat == "discrete":
    dist_list = discrete_dists

dist_name = st.sidebar.selectbox("", dist_list)
dist = get_dist(dist_name)


st.sidebar.write("## Set distribution parameters")

param_names = ls_params(dist)
param_dict = {}
for name in param_names:
    param_dict[name] = st.sidebar.number_input(
        f"{dist_name} [{name}]", value=float(param_val_default.get(name, 1)), step=0.1
    )


dist = dist(**param_dict)


st.write("## Density Plot")
cdf_flag = st.sidebar.checkbox("CDF")

st.sidebar.info('This app is developed by [Mark (Xin) Wang](mailto:wxgter@gmail.com")')

if dist_cat == "continuous":
    x = np.linspace(dist.ppf(0.005), dist.ppf(0.995), 100)
    if cdf_flag:
        y = dist.cdf(x)
    else:
        y = dist.pdf(x)

    df_plot = pd.DataFrame({"x": x, "density": y})
    fig = alt.Chart(df_plot).mark_line().encode(x="x", y="density")
elif dist_cat == "discrete":
    x = np.arange(dist.ppf(0.005), dist.ppf(0.995))
    if cdf_flag:
        y = dist.cdf(x)
    else:
        y = dist.pmf(x)

    df_plot = pd.DataFrame({"x": x, "density": y})
    fig = alt.Chart(df_plot).mark_bar().encode(alt.X("x", axis=alt.Axis(tickMinStep=1)), alt.Y("density"))

st.altair_chart(fig, use_container_width=True)


scipy_link = f"https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.{dist_name}.html"

if st.button(f"🚀{dist_name} doc"):
    webbrowser.open_new_tab(scipy_link)
