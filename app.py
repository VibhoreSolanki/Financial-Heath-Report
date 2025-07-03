import streamlit as st
import yfinance as yf
from fpdf import FPDF
import matplotlib.pyplot as plt

# ✅ Full verified NSE tickers that work on Yahoo Finance
ALL_TICKERS = sorted([
    "ASIANPAINT.NS", "TATAMOTORS.NS", "RELIANCE.NS", "HDFCBANK.NS", "ITC.NS",
    "INFY.NS", "SBIN.NS", "ADANIENT.NS", "ULTRACEMCO.NS", "LT.NS",
    "WIPRO.NS", "TECHM.NS", "MARUTI.NS", "DMART.NS", "COALINDIA.NS",
    "ONGC.NS", "JSWSTEEL.NS", "HCLTECH.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS",
    "ICICIBANK.NS", "DIVISLAB.NS", "SUNPHARMA.NS", "BHARTIARTL.NS", "KOTAKBANK.NS",
    "POWERGRID.NS", "TCS.NS", "NTPC.NS", "HINDUNILVR.NS", "HINDALCO.NS",
    "BPCL.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS", "GRASIM.NS", "INDUSINDBK.NS",
    "CIPLA.NS", "ADANIPORTS.NS", "EICHERMOT.NS", "BRITANNIA.NS", "TITAN.NS",
    "HEROMOTOCO.NS", "SHREECEM.NS", "UPL.NS", "TATACONSUM.NS", "TATASTEEL.NS",
    "HDFCLIFE.NS", "SBILIFE.NS", "BAJAJHLDNG.NS", "M&M.NS", "NESTLEIND.NS",
    "PIDILITIND.NS", "DRREDDY.NS", "AMBUJACEM.NS", "ABB.NS", "ATGL.NS",
    "BANDHANBNK.NS", "BERGEPAINT.NS", "BEL.NS", "CANBK.NS", "CHOLAFIN.NS",
    "DABUR.NS", "GAIL.NS", "GODREJCP.NS", "HAVELLS.NS", "ICICIPRULI.NS",
    "IDFCFIRSTB.NS", "IOC.NS", "JINDALSTEL.NS", "LUPIN.NS", "MUTHOOTFIN.NS",
    "OBEROIRLTY.NS", "PNB.NS", "RECLTD.NS", "SRF.NS", "TRENT.NS",
    "TVSMOTOR.NS", "UNIONBANK.NS", "VOLTAS.NS", "ZOMATO.NS", "NAVINFLUOR.NS",
    "TIINDIA.NS", "ESCORTS.NS", "GUJGASLTD.NS", "GLENMARK.NS", "IGL.NS",
    "AUBANK.NS", "ALKEM.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", "CUMMINSIND.NS",
    "FORTIS.NS", "GMRINFRA.NS", "IDBI.NS", "IRCTC.NS", "JSWENERGY.NS",
    "MINDTREE.NS", "NMDC.NS", "PERSISTENT.NS", "POLYCAB.NS", "RAJESHEXPO.NS",
    "SAIL.NS", "TATAPOWER.NS", "UCOBANK.NS", "UJJIVANSFB.NS", "YESBANK.NS",
    "ZYDUSLIFE.NS", "BALKRISIND.NS", "BATAINDIA.NS", "BANKINDIA.NS", "BLUEDART.NS",
    "BSOFT.NS", "CASTROLIND.NS", "CONCOR.NS", "CREDITACC.NS", "CROMPTON.NS",
    "DCBBANK.NS", "EXIDEIND.NS", "FEDERALBNK.NS", "FINEORG.NS", "GODREJPROP.NS",
    "HATSUN.NS", "HFCL.NS", "HINDCOPPER.NS", "IIFL.NS", "INDIGO.NS",
    "INDOSTAR.NS", "JUBLFOOD.NS", "LALPATHLAB.NS", "LINDEINDIA.NS", "MAHINDCIE.NS",
    "METROPOLIS.NS", "MOTILALOFS.NS", "MRPL.NS", "NATIONALUM.NS", "NAUKRI.NS",
    "PGHL.NS", "PRAJIND.NS", "PRINCEPIPE.NS", "RBLBANK.NS", "RENUKA.NS",
    "SBICARD.NS", "SHRIRAMFIN.NS", "SPARC.NS", "STLTECH.NS", "SYNGENE.NS",
    "TATACHEM.NS", "TCIEXP.NS", "TRIDENT.NS", "TTKPRESTIG.NS", "VGUARD.NS",
    "VINATIORGA.NS", "WHIRLPOOL.NS", "ZEEL.NS", "CENTURYTEX.NS", "CESC.NS",
    "EIDPARRY.NS", "ENGINERSIN.NS", "FSL.NS", "GESHIP.NS", "GODFRYPHLP.NS",
    "HINDPETRO.NS", "INDIACEM.NS", "IRFC.NS", "ISEC.NS", "JUBLINGREA.NS",
    "KEI.NS", "MAHABANK.NS", "MANGCHEFER.NS", "MCX.NS", "NETWORK18.NS",
    "NHPC.NS", "OIL.NS", "PETRONET.NS", "PNBHOUSING.NS", "RITES.NS",
    "RVNL.NS", "SJVN.NS", "TANLA.NS", "TATAELXSI.NS", "THYROCARE.NS",
    "TORNTPOWER.NS", "UJJIVAN.NS", "VAKRANGEE.NS", "WELCORP.NS", "WELSPUNIND.NS"
    "AARTIDRUGS.NS", "AARTIIND.NS", "ADANIGREEN.NS", "ADANITRANS.NS", "AFFLE.NS",
    "AJANTPHARM.NS", "ALKYLAMINE.NS", "AMARAJABAT.NS", "ANURAS.NS", "APLAPOLLO.NS",
    "APOLLOHOSP.NS", "APOLLOTYRE.NS", "ARVINDFASN.NS", "ASAHIINDIA.NS", "ASHOKLEY.NS",
    "ASTRAZEN.NS", "ASTRAL.NS", "ATUL.NS", "AUROPHARMA.NS", "AVANTIFEED.NS",
    "BALAMINES.NS", "BALRAMCHIN.NS", "BASF.NS", "BAYERCROP.NS", "BEML.NS",
    "BHEL.NS", "BIOCON.NS", "BIRLACORPN.NS", "BODALCHEM.NS", "BOMDYEING.NS",
    "BORORENEW.NS", "BRIGADE.NS", "CADILAHC.NS", "CAPLIPOINT.NS", "CARBORUNIV.NS",
    "CEATLTD.NS", "CENTRALBK.NS", "CENTURYPLY.NS", "CERA.NS", "CGPOWER.NS",
    "CHEMPLASTS.NS", "CHENNPETRO.NS", "COCHINSHIP.NS", "COFORGE.NS", "COLPAL.NS",
    "COROMANDEL.NS", "CUB.NS", "CYIENT.NS", "DBCORP.NS", "DCMSHRIRAM.NS",
    "DELTACORP.NS", "DEVYANI.NS", "DHANI.NS", "DISHTV.NS", "DIXON.NS",
    "ECLERX.NS", "EDELWEISS.NS", "EICHERMOT.NS", "EMAMILTD.NS", "ENDURANCE.NS",
    "EPL.NS", "ERIS.NS", "EVEREADY.NS", "EVERESTIND.NS", "FACT.NS",
    "FCONSUMER.NS", "FINCABLES.NS", "FINEOTEX.NS", "FLUOROCHEM.NS", "FMGOETZE.NS",
    "GEPIL.NS", "GHCL.NS", "GICRE.NS", "GILLETTE.NS", "GLAXO.NS",
    "GNFC.NS", "GODREJAGRO.NS", "GPIL.NS", "GREAVESCOT.NS", "GREENPLY.NS",
    "GRINDWELL.NS", "GSFC.NS", "GSKCONS.NS", "GULFOILLUB.NS", "HCG.NS",
    "HEG.NS", "HEIDELBERG.NS", "HERITGFOOD.NS", "HFCL.NS", "HIKAL.NS",
    "HIMATSEIDE.NS", "HINDZINC.NS", "HSCL.NS", "IEX.NS", "IFBIND.NS",
    "IGARASHI.NS", "IIFLWAM.NS", "IL&FSTRANS.NS", "IMFA.NS", "INDHOTEL.NS",
    "INDIAMART.NS", "INDIGOPNTS.NS", "INDOSTAR.NS", "INDTERRAIN.NS", "INSECTICID.NS",
    "INTELLECT.NS", "IRB.NS", "ISGEC.NS", "ITI.NS", "JAGRAN.NS",
    "JAICORPLTD.NS", "JAMNAAUTO.NS", "JBCHEPHARM.NS", "JCHAC.NS", "JINDALPOLY.NS",
    "JKCEMENT.NS", "JKLAKSHMI.NS", "JKPAPER.NS", "JKTYRE.NS", "JSL.NS",
    "JTEKTINDIA.NS", "JUBLINGREA.NS", "JYOTHYLAB.NS", "KALPATPOWR.NS", "KANSAINER.NS",
    "KARURVYSYA.NS", "KCP.NS", "KDDL.NS", "KEC.NS", "KIRLOSENG.NS",
    "KNRCON.NS", "KPRMILL.NS", "KRBL.NS", "LAXMIMACH.NS", "LEMONTREE.NS",
    "LINCOLN.NS", "LTI.NS", "LTTS.NS", "LUXIND.NS", "MAHINDCIE.NS"
    "MAHSCOOTER.NS", "MANAPPURAM.NS", "MARKSANS.NS", "MASTEK.NS", "MAZDOCK.NS",
    "MEGH.NS", "MINDACORP.NS", "MOIL.NS", "MPHASIS.NS", "MRF.NS",
    "MSTCLTD.NS", "NATCOPHARM.NS", "NBCC.NS", "NBVENTURES.NS", "NCC.NS",
    "NEULANDLAB.NS", "NFL.NS", "NH.NS", "NILKAMAL.NS", "NRBBEARING.NS",
    "NSLNISP.NS", "NUCLEUS.NS", "OLECTRA.NS", "ORIENTCEM.NS", "ORIENTELEC.NS",
    "PAGEIND.NS", "PCBL.NS", "PFIZER.NS", "PHOENIXLTD.NS", "PIIND.NS",
    "PILITA.NS", "PILANIINV.NS", "PRAKASH.NS", "PRSMJOHNSN.NS", "PTC.NS",
    "QUESS.NS", "RADICO.NS", "RAIN.NS", "RAMCOCEM.NS", "RALLIS.NS",
    "RATNAMANI.NS", "RCF.NS", "REDINGTON.NS", "RELAXO.NS", "REPCOHOME.NS",
    "RICOAUTO.NS", "ROUTE.NS", "RTNINDIA.NS", "RVNL.NS", "SADBHAV.NS",
    "SANSERA.NS", "SANOFI.NS", "SASTASUNDR.NS", "SBC.NS", "SCHAEFFLER.NS",
    "SCI.NS", "SEQUENT.NS", "SESHAPAPER.NS", "SHK.NS", "SHOPERSTOP.NS",
    "SHYAMMETL.NS", "SIS.NS", "SJS.NS", "SKFINDIA.NS", "SOLARA.NS",
    "SONATSOFTW.NS", "SOUTHBANK.NS", "SPANDANA.NS", "SPENCERS.NS", "SPICEJET.NS",
    "SPTL.NS", "STAR.NS", "STEL.NS", "STERTOOLS.NS", "SUBEXLTD.NS",
    "SUDARSCHEM.NS", "SUVENPHAR.NS", "SWANENERGY.NS", "TASTYBITE.NS", "TCNSBRANDS.NS",
    "TCPLPACK.NS", "TEAMLEASE.NS", "TEGA.NS", "TEXRAIL.NS", "THEINVEST.NS",
    "THERMAX.NS", "THOMASCOOK.NS", "THYROCARE.NS", "TIDEWATER.NS", "TIMETECHNO.NS",
    "TIRUMALCHM.NS", "TITAGARH.NS", "TNPL.NS", "TOKYOPLAST.NS", "TORNTPHARM.NS",
    "TPLPLASTEH.NS", "TRANSCHEM.NS", "TRF.NS", "TRIVENI.NS", "TTML.NS",
    "TV18BRDCST.NS", "TVTODAY.NS", "UBL.NS", "UCALFUEL.NS", "UFLEX.NS",
    "UGARSUGAR.NS", "UJJIVANSFB.NS", "UMAEXPORTS.NS", "UNIDT.NS", "UNIVCABLES.NS",
    "UTIAMC.NS", "VAIBHAVGBL.NS", "VARROC.NS", "VASWANI.NS", "VBL.NS",
    "VENKEYS.NS", "VETO.NS", "VGUARD.NS", "VISHNU.NS", "VISHWARAJ.NS",
    "VMART.NS", "VOLTAMP.NS", "VRLLOG.NS", "VSSL.NS", "WABAG.NS",
    "WABCOINDIA.NS", "WANBURY.NS", "WATERBASE.NS", "WEIZMANIND.NS", "WELENT.NS",
    "WESTLIFE.NS", "WHEELS.NS", "WIPRO.NS", "WONDERLA.NS", "WSTCSTPAPR.NS",
    "XCHANGING.NS", "YESBANK.NS", "ZEELEARN.NS", "ZEEMEDIA.NS", "ZENSARTECH.NS",
    "ZODIACLOTH.NS", "ZYDUSWELL.NS", "21STCENMGM.NS", "3IINFOTECH.NS", "3MINDIA.NS",
    "63MOONS.NS", "A2ZINFRA.NS", "AAKASH.NS", "AARON.NS", "AARTISURF.NS",
    "AAVAS.NS", "ABAN.NS", "ABBOTINDIA.NS", "ABCAPITAL.NS", "ABFRL.NS",
    "ACC.NS", "ACCELYA.NS", "ACCURACY.NS", "ACE.NS", "ADFFOODS.NS",
    "ADORWELD.NS", "ADVANIHOTR.NS", "AEGISCHEM.NS", "AFFLE.NS", "AGARIND.NS"
    "AGRITECH.NS", "AHLADA.NS", "AHLEAST.NS", "AHLUCONT.NS", "AIAENG.NS",
    "AIRAN.NS", "AJRINFRA.NS", "AKASH.NS", "AKZOINDIA.NS", "ALANKIT.NS",
    "ALBERTDAVD.NS", "ALCHEM.NS", "ALEMBICLTD.NS", "ALICON.NS", "ALKALI.NS",
    "ALLCARGO.NS", "ALLSEC.NS", "ALOKINDS.NS", "ALPHAGEO.NS", "AMBER.NS",
    "AMJLAND.NS", "ANDHRAPAP.NS", "ANDHRSUGAR.NS", "ANGELONE.NS", "ANIKINDS.NS",
    "ANSALAPI.NS", "ANTGRAPHIC.NS", "APCOTEXIND.NS", "APEX.NS", "APLAPOLLO.NS",
    "APLLTD.NS", "APOLLO.NS", "APOLLOPIPE.NS", "APTUS.NS", "ARCHIDPLY.NS",
    "ARENTERP.NS", "ARIES.NS", "ARSSINFRA.NS", "ARTEMISMED.NS", "ARTNIRMAN.NS",
    "ARVEE.NS", "ARVIND.NS", "ASAHISONG.NS", "ASAL.NS", "ASHAPURMIN.NS",
    "ASHIMASYN.NS", "ASIANENE.NS", "ASIANHOTNR.NS", "ASPINWALL.NS", "ASTEC.NS",
    "ASTRAMICRO.NS", "ATHARVENT.NS", "ATLANTA.NS", "ATULAUTO.NS", "AUBANK.NS",
    "AURIONPRO.NS", "AUTOAXLES.NS", "AUTOIND.NS", "AVADHSUGAR.NS", "AVANTEL.NS",
    "AXITA.NS", "AYMSYNTEX.NS", "BAFNAPH.NS", "BAGFILMS.NS", "BAJAJCON.NS",
    "BAJAJELEC.NS", "BAJAJHCARE.NS", "BALAJITELE.NS", "BALPHARMA.NS", "BANG.NS",
    "BANKBARODA.NS", "BANSWRAS.NS", "BARBEQUE.NS", "BASF.NS", "BATAINDIA.NS",
    "BAYERCROP.NS", "BBL.NS", "BCLIND.NS", "BCP.NS", "BEML.NS",
    "BENGALASM.NS", "BERGEPAINT.NS", "BHAGCHEM.NS", "BHAGERIA.NS", "BHAGYANGR.NS",
    "BHANDARI.NS", "BHARATFORG.NS", "BHARATRAS.NS", "BHEL.NS", "BIGBLOC.NS",
    "BIL.NS", "BINANIIND.NS", "BINDALAGRO.NS", "BIRLAMONEY.NS", "BKMINDST.NS",
    "BLISSGVS.NS", "BLS.NS", "BOMDYEING.NS", "BOROLTD.NS", "BPL.NS",
    "BRFL.NS", "BRIGADE.NS", "BRNL.NS", "BROOKS.NS", "BSE.NS",
    "BSHSL.NS", "BSL.NS", "BUTTERFLY.NS", "CADSYS.NS", "CALSOFT.NS",
    "CAMLINFINE.NS", "CAPACITE.NS", "CAPTRUST.NS", "CARERATING.NS", "CARYSIL.NS",
    "CASTROLIND.NS", "CENTENKA.NS", "CENTEXT.NS", "CENTUM.NS", "CERA.NS",
    "CEREBRAINT.NS", "CGCL.NS", "CHALET.NS", "CHEMFAB.NS", "CHEMPLASTS.NS",
    "CHEMTEX.NS", "CHEVIOT.NS", "CHOLAHLDNG.NS", "CIGNITITEC.NS", "CINELINE.NS",
    "CINEVISTA.NS", "CLNINDIA.NS", "COCHINSHIP.NS", "COFFEEDAY.NS", "CONTROLPR.NS",
    "CORALFINAC.NS", "CORDSCABLE.NS", "COROMANDEL.NS", "COSMOFILMS.NS", "COUNCODOS.NS",
    "CREATIVE.NS", "CREST.NS", "CUBEXTUB.NS", "CUPID.NS", "CYBERMEDIA.NS",
    "CYIENT.NS", "DABUR.NS", "DALMIASUG.NS", "DAMODARIND.NS", "DATAMATICS.NS",
    "DBREALTY.NS", "DBSTOCKBRO.NS", "DCAL.NS", "DCMSHRIRAM.NS", "DCW.NS"
])
ticker = st.selectbox("Select company", sorted(ALL_TICKERS))

# Generate AI-style summary
def generate_summary(ticker, pe, de):
    summary = [f"**{ticker} Financial Snapshot**"]
    if pe is not None:
        if pe > 25:
            summary.append("🔴 Very high P/E — likely overvalued")
        elif pe < 10:
            summary.append("🟢 Low P/E — possibly undervalued")
        else:
            summary.append("🟡 Fairly valued based on P/E")
    if de is not None:
        if de > 2:
            summary.append("🔴 High debt-to-equity — leverage risk")
        else:
            summary.append("🟢 Healthy leverage")
    summary.append("📌 Always compare against sector peers.")
    return "\n".join(summary)

# Create a downloadable PDF report
def create_pdf(ticker, pe, de, summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"{ticker} Report", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"P/E: {pe}", ln=True)
    pdf.cell(0, 10, f"D/E: {de}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, summary)
    file_name = f"{ticker}_report.pdf"
    pdf.output(file_name)
    return file_name

# Streamlit App UI
st.set_page_config(page_title="NSE Finance Dashboard", layout="centered")
st.title("📈 Financial Health Report ")

# Top-right contact info using columns
col1, col2 = st.columns([3, 1])  # 3:1 ratio to push content to right

with col2:
    st.markdown("""
    <div style='text-align: right; font-size: 14px; line-height: 1.8; white-space: nowrap;'>
        🙋‍♂️ <b>Created by: Vibhore Solanki</b><br>
        📧 <a href='https://mail.google.com/mail/?view=cm&to=cavibhoresolanki@gmail.com' target='_blank'>cavibhoresolanki@gmail.com</a><br>
        🔗 <a href='https://www.linkedin.com/in/vibhoresolanki' target='_blank'>LinkedIn</a>
    </div>
    """, unsafe_allow_html=True)



 
if st.button("Generate Report"):

    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="5y")

        if not info or 'longName' not in info:
            st.warning(f"⚠️ Could not fetch data for {ticker}. Try another one.")
        else:
            st.success(f"✅ Fetched data for {info['longName']}")

            # 📈 Price Chart
            st.subheader("📈 5 Year Price Chart")
            if not hist.empty:
                st.line_chart(hist["Close"])
            else:
                st.warning("No price data available.")

            # 📌 Key Metrics
            st.subheader("📌 Key Metrics")
            st.write(f"**Sector:** {info.get('sector', 'N/A')}")
            st.write(f"**Market Cap:** ₹{info.get('marketCap', 'N/A'):,}")
            st.write(f"**PE Ratio:** {info.get('trailingPE', 'N/A')}")
            st.write(f"**ROE:** {info.get('returnOnEquity', 'N/A')}")
            st.write(f"**Debt/Equity:** {info.get('debtToEquity', 'N/A')}")
            st.write(f"**Profit Margin:** {info.get('profitMargins', 'N/A')}")

            # 🚩 Red Flags
            st.subheader("🚩 Red Flags")
            red_flags = []
            if info.get('debtToEquity', 0) > 1.5:
                red_flags.append("High Debt-to-Equity Ratio")
            if info.get('profitMargins', 0) < 0.05:
                red_flags.append("Low Profit Margins")
            if info.get('returnOnEquity', 0) < 0.08:
                red_flags.append("Weak ROE")

            if red_flags:
                for flag in red_flags:
                    st.warning(f"• {flag}")
            else:
                st.success("✅ No major red flags detected.")

            # 🧠 AI Summary
            st.subheader("🧠 AI Analysis Summary")
            summary_lines = [
                f"{info['longName']} is a {info.get('sector', 'N/A')} sector company.",
                f"It currently has a market capitalization of ₹{info.get('marketCap', 0):,}.",
                "",
                f"The company’s PE ratio is {info.get('trailingPE', 'N/A')}, indicating it may be "
                + ("overvalued" if info.get('trailingPE', 0) > 25 else "undervalued") + " compared to peers.",
                "",
                f"ROE of {info.get('returnOnEquity', 'N/A')} and Profit Margin of {info.get('profitMargins', 'N/A')} "
                + "highlight its " + ("strong" if info.get('profitMargins', 0) > 0.1 else "weak") + " profitability."
            ]
            st.info("\n".join(summary_lines))

            # 📌 Final Disclaimer
            st.markdown("---")
            st.markdown("📌 _This is an auto-generated report. Please verify independently before making financial decisions._", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"🚨 Error: {e}")
