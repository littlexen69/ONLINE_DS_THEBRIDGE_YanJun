import pandas as pd

def limpieza_phishing(dict):
    df = pd.DataFrame([dict])
    df['HasPopup'] = (df['NoOfPopup'] >= 1).astype(int)
    df["Nivel3_Alta"] = ((df["IsDomainIP"] == 1) |((df["HasPasswordField"] == 1) & (df["IsHTTPS"] == 0)) |(df["HasExternalFormSubmit"] == 1)).astype(int)
    df["Nivel2_Media"] = ((df["ObfuscationRatio"] > 0.2) |(df["DomainLength"] > 25) |(df["NoOfSubDomain"] > 3)).astype(int)
    df["Nivel1_Baja"] = ((df["DomainTitleMatchScore"] < 1.0) |(df["TLDLegitimateProb"] < 0.25) |(df["NoOfPopup"] > 0)).astype(int)
    df_r = df[["DomainLength",
               "IsDomainIP",
               'NoOfSubDomain',
               'HasObfuscation',
               'ObfuscationRatio',
               'CharContinuationRate',
               'TLDLegitimateProb',
               'URLCharProb',
               'HasPasswordField',
               'IsHTTPS',
               'HasExternalFormSubmit',
               'DomainTitleMatchScore',
               'HasPopup',
               'NoOfiFrame',
               'Bank',
               'Pay',
               'Crypto',
               'DomainTitleMatchScore',
               'URLTitleMatchScore',
               'Nivel3_Alta',
               'Nivel2_Media',
               'Nivel1_Baja']]
    df_r['IsPhishing'] = ((df['Nivel3_Alta'] == 1) | (df['Nivel2_Media'] == 1) | (df['Nivel1_Baja'] == 1)).astype(int)
    return df_r