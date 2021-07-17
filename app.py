import pandas as pd
import numpy as np
import streamlit as st
import scipy.stats as ss
import altair as alt


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


def gen_x(dist, is_continuous, ql=0.005, qr=0.995, n=500):
    if is_continuous:
        x = np.linspace(dist.ppf(ql), dist.ppf(qr), n)
    else:
        x = np.arange(dist.ppf(ql), dist.ppf(qr))
    return x


def gen_y(dist, x, is_continuous, is_cdf):
    if is_cdf:
        y = dist.cdf(x)
    else:
        if is_continuous:
            y = dist.pdf(x)
        else:
            y = dist.pmf(x)
    return y


def gen_fig(df, is_continuous):
    fig = alt.Chart(df)
    yaxis = alt.Y("y", axis=alt.Axis(title=""))

    if is_continuous:
        fig = fig.mark_line().encode(alt.X("x", axis=alt.Axis(title="")), yaxis)
    else:
        fig = fig.mark_bar().encode(alt.X("x", axis=alt.Axis(tickMinStep=1, title="")), yaxis)
    return fig


continuous_dists = get_continuous_dist()
discrete_dists = get_discrete_dist()


st.sidebar.info(
    """
    🎈 A streamlit app for visualising [`scipy.stats`](https://docs.scipy.org/doc/scipy/reference/stats.html) 
    univariate distributions, developed by [Mark (Xin) Wang](mailto:wxgter@gmail.com").
    """
)

st.sidebar.write("## Select distribution")
dist_cat = st.sidebar.radio("", ["continuous", "discrete"])
continous_flag = dist_cat == "continuous"

param_default = dict(loc=0, scale=1, p=0.5)

if continous_flag:
    dist_list = continuous_dists
else:
    dist_list = discrete_dists

dist_name = st.sidebar.selectbox("", dist_list)
dist = get_dist(dist_name)

scipy_link = f"https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.{dist_name}.html"
st.sidebar.markdown(f"[`scipy.stats.{dist_name}`]({scipy_link})")

st.sidebar.write("## Set parameters")

param_dict = {
    p: st.sidebar.number_input(f"{dist_name} [{p}]", value=float(param_default.get(p, 1)), step=0.1)
    for p in ls_params(dist)
}


dist = dist(**param_dict)

cdf_flag = st.sidebar.checkbox("CDF")


x = gen_x(dist, continous_flag)
y = gen_y(dist, x, continous_flag, cdf_flag)
df = pd.DataFrame({"x": x, "y": y})


st.markdown("## Code Snippet")
param_str = str(param_dict)[1:-1].replace(":", "=").replace("'", "").replace("= ", "=")

st.code(
    f"""from scipy.stats import {dist_name}

rv = {dist_name}({param_str})
"""
)
st.write("## Density Plot")
st.altair_chart(gen_fig(df, continous_flag), use_container_width=True)
