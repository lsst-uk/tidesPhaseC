"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import hmac
import pandas as pd
from io import StringIO
import numpy as np

st.set_page_config(layout="wide")



def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


# if not check_password():
#     st.stop()

st.title('TiDES Manual Upload')

st.write("Please use this web page to manually upload targets to the TiDES targets manager. This targets will then be sent to 4MOST on the next upload cycle.")

with st.expander("Click here to see columns accepted by 4MOST "):
  st.html(
      """
  <table width="621" cellpadding="7" cellspacing="0">
    <col width="162"/>

    <col width="150"/>

    <col width="171"/>

    <col width="170"/>

    <tr valign="top">
      <td width="162" bgcolor="#a6a6a6" style="background: #a6a6a6; border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <b><font size="2" style="font-size: 11pt">Column Name</font></b></p>
      </td>
      <td width="60" bgcolor="#a6a6a6" style="background: #a6a6a6; border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <b><font size="2" style="font-size: 11pt">Type</font></b></p>
      </td>
      <td width="171" bgcolor="#a6a6a6" style="background: #a6a6a6; border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <b><font size="2" style="font-size: 11pt">Description</font></b></p>
      </td>
      <td width="170" bgcolor="#a6a6a6" style="background: #a6a6a6; border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <b><font size="2" style="font-size: 11pt">Notes</font></b></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">NAME</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">String</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">(up to 256 chars)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Human readable target
        identifier. As supplied by the science team.</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Required to be unique for
        each target within a sub-survey (uniqueness exception:
        transients), and must be</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">alphanumeric.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" height="25" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">RA</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1D, double)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Right Ascension, in units
        decimal degrees (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>deg</b></font></font><font size="2" style="font-size: 11pt">)</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p align="left" style="orphans: 0; widows: 0; margin-top: 0.11cm; margin-bottom: 0.21cm">
        <font size="2" style="font-size: 11pt">Range: 0 to 359.99999999</font></p>
        <p align="left" style="orphans: 0; widows: 0; margin-top: 0.11cm"><font size="2" style="font-size: 11pt">Note:
        must have at least 3 decimal digits, preferably 5+</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" height="20" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">DEC</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Float (1D, double)</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <br/>

        </p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Declination, in units
        decimal degrees (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>deg</b></font></font><font size="2" style="font-size: 11pt">)</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p align="left" style="orphans: 0; widows: 0; margin-top: 0.11cm; margin-bottom: 0.21cm">
        <font size="2" style="font-size: 11pt">Range: -89.99999999 to +40</font></p>
        <p align="left" style="orphans: 0; widows: 0; margin-top: 0.11cm"><font size="2" style="font-size: 11pt">Note:
        must have at least 3 decimal digits, preferably 5+</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">PMRA</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Proper motion wrt. RA, in
        units mas/yr (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>mas/yr</b></font></font><font size="2" style="font-size: 11pt">)</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: -1e6 to +1e6</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Undefined values should be
        set to 0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">PMDEC</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Proper motion wrt. DEC, in
        units mas/yr (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>mas/yr</b></font></font><font size="2" style="font-size: 11pt">)</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: -1e6 to +1e6</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Undefined values should be
        set to 0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">EPOCH</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Epoch of coordinate
        position, in units Julian Date (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>yr</b></font></font><font size="2" style="font-size: 11pt">)</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 1950 to
        2050<br/>
  Example: 2016.0, e.g. GAIA DR3.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">See below about usage.</font><sup><font size="2" style="font-size: 11pt">9</font></sup></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">RESOLUTION</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Integer (1I, short int)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Desired resolution mode for
        this target</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Options:</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
          <font size="2" style="font-size: 11pt">1: LRS</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
          <font size="2" style="font-size: 11pt">2: HRS</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">SUBSURVEY</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">String</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">(up to 256 chars)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Sub-survey name for
        target’s membership</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Alphanumeric</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">CADENCE</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Integer (int64, long long
        int)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">An integer that encodes
        information regarding observing cadence.</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 0 to (2**22 – 1).</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">See below for details about
        encoding.</font><sup><font size="2" style="font-size: 11pt">1</font></sup></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">TEMPLATE</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">String</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">(up to 256 chars)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Spectral template filename
        describing the predicted spectral shape of this target,</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Alphanumeric, see also §7.3
        of the 4FS-WI User Manual.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">RULESET</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">String</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">(up to 256 chars)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Name of the ruleset
        describing the target’s spectral success criteria.</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">This should be the named
        ruleset and not the filename containing possibly multiple
        rulesets.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Alphanumeric, must begin
        with a letter. See also §7.4.2 of the 4FS-WI User Manual.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">REDSHIFT_ESTIMATE</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Estimated redshift of
        target at time of targeting (e.g. from photo-z)</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: -0.01 to 10.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">See below about usage.</font><sup><font size="2" style="font-size: 11pt">4</font></sup></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">REDSHIFT_ERROR</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">1 sigma uncertainty in
        REDSHIFT</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Range: 0 to 10.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">EXTENT_FLAG</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Integer (1I, short int)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Flag defining the model to
        compute the flux.</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Options:</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
          <font size="2" style="font-size: 11pt">0: POINT SOURCE;</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
          <font size="2" style="font-size: 11pt">1: Box/Flat;</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
          <font size="2" style="font-size: 11pt">2: Sersic profile.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">See below for details.</font><sup><font size="2" style="font-size: 11pt">2</font></sup></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">EXTENT_PARAMETER</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Integer or Float (1I or 1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Parameter describing the
        spatial extent (radius) of the </font><font size="2" style="font-size: 11pt">Sersic
        profile in units arcsec (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>arcsec</b></font></font><font size="2" style="font-size: 11pt">).</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Ignored if not
        EXTENT_FLAG=2 (Sersic profile).</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 0.1 to 100.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">See below for details.</font><sup><font size="2" style="font-size: 11pt">2</font></sup></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">EXTENT_INDEX</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Integer or Float (1I or 1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Index of the Sersic profile</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Ignored if not
        EXTENT_FLAG=2 (Sersic profile).</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 0.1 to 10.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">See below for details.</font><sup><font size="2" style="font-size: 11pt">2</font></sup></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">MAG</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Apparent magnitude for the
        target already reddened, in units magnitude (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>mag</b></font></font><font size="2" style="font-size: 11pt">).</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-left: 0.19cm">
        <br/>

        </p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Magnitude should be
        consistent with the MAG_TYPE column and its band.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 3 to 50.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Note that usage depends on
        EXTENT_FLAG.</font><sup><font size="2" style="font-size: 11pt">2</font></sup></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">MAG_ERR</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">1 sigma uncertainty on
        entries in MAG column, in units magnitude (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>mag</b></font></font><font size="2" style="font-size: 11pt">)</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 0 to 50.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Can be zero or NULL; not
        currently used</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">MAG_TYPE</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">String</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">(up to 256 chars)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Identifier for the
        magnitude or flux density system which describes the MAG and
        TEMPLATE columns.</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Only a limited set of
        standard “Filters” and standard “Systems” are accepted,
        see below for options.</font><sup><font size="2" style="font-size: 11pt">3</font></sup></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">REDDENING</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Foreground reddening E(B-V)
        to apply to the template, in units magnitude (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>mag</b></font></font><font size="2" style="font-size: 11pt">).</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 0 to 100.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Can be zero or NAN.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage.</font><sup><font size="2" style="font-size: 11pt">4</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Modified in FMTVERS=2.0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">TEMPLATE_REDSHIFT</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Redshift used by template.</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: -0.1 to 10.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage.</font><sup><font size="2" style="font-size: 11pt">4</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">DATE_EARLIEST</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Earliest date when this
        target can be observed, in units days  (as </font><font size="2" style="font-size: 11pt"><b>d</b></font><font size="2" style="font-size: 11pt">).</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Julian Date (decimal days).
        See below about usage.</font><sup><font size="2" style="font-size: 11pt">5</font></sup></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">DATE_LATEST</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Latest date when this
        target can be observed, in units days  (as </font><font size="2" style="font-size: 11pt"><b>d</b></font><font size="2" style="font-size: 11pt">).</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Julian Date (decimal days).
        See below about usage.</font><sup><font size="2" style="font-size: 11pt">5</font></sup></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">CAL_MAG_BLUE</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Apparent magnitude to
        suggest for object during fibre calibration in the blue arm, in
        units magnitude (as </font><font size="2" style="font-size: 11pt"><b>mag</b></font><font size="2" style="font-size: 11pt">).</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 0 to 50.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage.</font><sup><font size="2" style="font-size: 11pt">6</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">CAL_MAG_ERR_BLUE</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">1 sigma uncertainty on
        entries in CAL_MAG_BL</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">column, in units magnitude
        (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>mag</b></font></font><font size="2" style="font-size: 11pt">).</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 0 to 50.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage.</font><sup><font size="2" style="font-size: 11pt">6</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">CAL_MAG_ID_BLUE</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">String (up to 256 chars)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Identifier for the
        magnitude system which describes the CAL_MAG_BL.</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage and
        acceptable options.</font><sup><font size="2" style="font-size: 11pt">6</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">CAL_MAG_GREEN</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Apparent magnitude to
        suggest for object during fibre calibration in the green arm, in
        units magnitude (as </font><font size="2" style="font-size: 11pt"><b>mag</b></font><font size="2" style="font-size: 11pt">).</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 0 to 50.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage</font><sup><font size="2" style="font-size: 11pt">6</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">CAL_MAG_ERR_GREEN</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">1 sigma uncertainty on
        entries in CAL_MAG_GR</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">column, in units magnitude
        (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>mag</b></font></font><font size="2" style="font-size: 11pt">).</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 0 to 50.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage.</font><sup><font size="2" style="font-size: 11pt">6</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">CAL_MAG_ID_GREEN</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">String (up to 256 chars)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Identifier for the
        magnitude system which describes the CAL_MAG_GR.</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage and
        acceptable options.</font><sup><font size="2" style="font-size: 11pt">6</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">CAL_MAG_RED</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Apparent magnitude to
        suggest for object during fibre calibration in the blue arm, in
        units magnitude (as </font><font size="2" style="font-size: 11pt"><b>mag</b></font><font size="2" style="font-size: 11pt">).</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 0 to 50.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage.</font><sup><font size="2" style="font-size: 11pt">6</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">CAL_MAG_ERR_RED</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">1 sigma uncertainty on
        entries in CAL_MAG_RD</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">column, in units magnitude
        (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>mag</b></font></font><font size="2" style="font-size: 11pt">).</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 0 to 50.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage.</font><sup><font size="2" style="font-size: 11pt">6</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">CAL_MAG_ID_RED</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">String (up to 256 chars)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Identifier for the
        magnitude system which describes the CAL_MAG_RD.</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage and
        acceptable options.</font><sup><font size="2" style="font-size: 11pt">6</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.0.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">CLASSIFICATION</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">String (up to 256 chars)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Expected/estimated
        classification type(s) for target.</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage and
        acceptable options.</font><sup><font size="2" style="font-size: 11pt">7</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.2.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">COMPLETENESS</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Per-target completeness
        within sub-survey</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Range: 0.0 to 1.0.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">See below about usage.</font><sup><font size="2" style="font-size: 11pt">8</font></sup></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.3.</font></p>
      </td>
    </tr>
    <tr valign="top">
      <td width="162" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">PARALLAX</font></p>
      </td>
      <td width="60" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Float (1E)</font></p>
      </td>
      <td width="171" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 11pt">Stellar parallax of target,</font><font size="2" style="font-size: 11pt">
        in units milliarcseconds (as </font><font face="Courier New, serif"><font size="2" style="font-size: 11pt"><b>mas</b></font></font><font size="2" style="font-size: 11pt">).</font></p>
      </td>
      <td width="170" style="border: 1px solid #000000; padding: 0cm 0.19cm"><p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Required for 4MOST fibre
        positioning and CNAME definition.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2; margin-bottom: 0cm">
        <font size="2" style="font-size: 11pt">Undefined values should be
        set to 0.</font></p>
        <p lang="en-GB" class="western" align="left" style="orphans: 2; widows: 2">
        <font size="2" style="font-size: 10pt">Introduced in FMTVERS=2.5.</font></p>
      </td>
    </tr>
  </table>
  """
  )

## Here are the required formats:

## Here are the minimum required keywords
minimum_required_keywords = [
    "NAME",
    "RA",
    "DEC",
    "PMRA",
    "PMDEC",
    "EPOCH",
    "RESOLUTION",
    "SUBSURVEY",
    "TEMPLATE",
    "RULESET",
    "EXTENT_FLAG",
    "EXTENT_PARAMETER",
    "EXTENT_INDEX",
    "MAG_TYPE",
    "MAG",
    "MAG_ERR",
    "DATE_EARLIEST",
    "DATE_LATEST",
    "CADENCE",
    "REDDENING",
    "REDSHIFT_ESTIMATE",
    "REDSHIFT_ERROR",
    "TEMPLATE_REDSHIFT",
    "CAL_MAG_BLUE",
    "CAL_MAG_GREEN",
    "CAL_MAG_RED",
    "CAL_MAG_ERR_BLUE",
    "CAL_MAG_ERR_GREEN",
    "CAL_MAG_ERR_RED",
    "CAL_MAG_ID_BLUE",
    "CAL_MAG_ID_GREEN",
    "CAL_MAG_ID_RED",
    "CLASSIFICATION",
    "COMPLETENESS",
    "PARALLAX",
]

### use a dictionary to define expected data types
col_format = {
    'NAME':str,
    'RA':np.float64, 'DEC':np.float64,
    'PMRA':np.float32, 'PMDEC':np.float32,
    'EPOCH':np.float32, 'RESOLUTION':np.int16,
    'SUBSURVEY':str,
    'TEMPLATE':str, 'RULESET':str,
    'EXTENT_FLAG':np.int32,
    'EXTENT_PARAMETER':np.float32,'EXTENT_INDEX':np.float32,
    'MAG_TYPE':str,
    'MAG':np.float32,'MAG_ERR':np.float32,
    'DATE_EARLIEST':np.float64, 'DATE_LATEST':np.float64,
    'CADENCE':np.int64,
    'REDDENING':np.float32,
    'REDSHIFT_ESTIMATE':np.float32,
    'REDSHIFT_ERROR':np.float32,
    'CAL_MAG_ID_BLUE':str,
    'CAL_MAG_ID_GREEN':str,
    'CAL_MAG_ID_RED':str,
    'CLASSIFICATION':str,
    'COMPLETENESS':np.float32,
    'PARALLAX':np.float32,
}
# cFormat = pd.Series(col_format)
# print(cFormat)
## We need to check if the uploaded CSV file matches the 

uploaded_file = st.file_uploader("Choose a file")

convertedDtype = 0
meetMinFlag = 1
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    #st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    #st.write(dataframe)

    st.write('First 15 rows:')
    st.dataframe(dataframe[:15])

    st.title("Testing catalogue")

    #res = dataframe.dtypes
    
    meetMinimum = np.isin(np.array(minimum_required_keywords),dataframe.columns)

    #Check there are no Falses in the meetMinimum
    if np.sum(~meetMinimum)!=0:
        st.write('The following **required** columns are missing:')
        st.dataframe(pd.DataFrame(np.array(minimum_required_keywords)[~meetMinimum], columns=['COLUMN NAME']),use_container_width=True)
        meetMinFlag = 0
        st.write(":red[Please make the necesary changes to your catalogue and re-upload a file to try again.]")

    # Now we need to check that the columns that jhave data types match the required datatypes

    try:
        convertedDF = dataframe.astype(col_format)
        convertedDtype = 1
        st.title("Checking data")
        st.write("✅ Data types agree with 4MOST requirements")
    except Exception as e:
        st.title("❌ Cannot convert data to required data type")
        st.write("""Please check your data format.
        Error message: """)
        st.code(e,language='shellSession')
        st.write(":red[Please fix errors in catalogue and reupload.]")

st.title("Send catalogue to 4MOST")

readyBitFlip = 1 - (convertedDtype & meetMinFlag)
if readyBitFlip != 1:
  st.write("Your catalogue has passed all the necessary checks. You may now upload by clicking the button below.")
else:
  st.write("Upload diabled until catalogue changes made.")
# Create a button and disable it if it was clicked
st.button(
    f"Send catalogue to 4MOST",
    disabled= readyBitFlip
)
    
    #pd.testing.assert_series_equal(res,s)



