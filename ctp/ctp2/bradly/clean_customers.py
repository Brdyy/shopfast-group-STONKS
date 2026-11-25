#!/usr/bin/env python3
"""Nettoyage client pandas, équivalent aux opérations prescrites OpenRefine."""
from pathlib import Path
import re
import pandas as pd

HERE=Path(__file__).resolve().parent
INPUT=HERE/"shopfast-kit"/"data"/"customers.csv"
if not INPUT.exists(): INPUT=Path("/home/user/ctp2/shopfast-kit/data/customers.csv")
OUTPUT=HERE/"customers_clean.csv"
df=pd.read_csv(INPUT,dtype=str,keep_default_na=False)
initial=len(df)
# Étape 1: retirer uniquement les lignes strictement identiques, garder la première.
df=df.drop_duplicates(keep="first").copy()
removed=initial-len(df)
def norm_name(v): return re.sub(r"\s+"," ",v.strip()).title()
for c in ["first_name","last_name"]: df[c]=df[c].map(norm_name)
df["email"]=df.email.str.strip().str.lower()
country_map={"fr":"FR","france":"FR","fra":"FR","de":"DE","deu":"DE","germany":"DE","allemagne":"DE","es":"ES","españa":"ES","espagne":"ES","spain":"ES","be":"BE","bel":"BE","belgique":"BE","belgium":"BE","bel":"BE"}
df["country"]=df.country.str.strip().str.casefold().map(country_map).fillna("")
# Formats acceptés reproduisent les GREL examples et les dates courantes du fichier.
def iso_date(v):
    v=v.strip()
    if not v:return ""
    for fmt in ("%Y-%m-%d","%d/%m/%Y","%m-%d-%Y","%Y/%m/%d","%m/%d/%Y","%d-%m-%Y"):
        try:return pd.to_datetime(v,format=fmt,errors="raise").strftime("%Y-%m-%d")
        except (ValueError,TypeError):pass
    return v
for c in ["signup_date","birth_date"]: df[c]=df[c].map(iso_date)
df["loyalty_tier"]=df.loyalty_tier.str.strip().str.lower().replace({"platinium":"platinum"})
def postal(v,country):
    v=v.strip()
    return v.zfill(5) if country=="FR" and v.isdigit() and len(v)==4 else v
df["postal_code"]=[postal(p,c) for p,c in zip(df.postal_code,df.country)]
def phone(v):
    v=v.strip()
    if not v:return ""
    s=re.sub(r"[^0-9+]","",v)
    if s.startswith("0033"): return "+33"+s[4:]
    if s.startswith("00"): return "+"+s[2:]
    if s.startswith("0") and len(s)==10:return "+33"+s[1:]
    return s
df["phone"]=df.phone.map(phone)
# Flaguer toutes les occurrences d'un email dupliqué; les emails vides ne sont pas des doublons.
nonblank=df.email.ne("")
dupmask=nonblank & df.email.duplicated(keep=False)
df["is_duplicate_email"]=dupmask
# Strings, booléen explicite.
df["is_duplicate_email"]=df.is_duplicate_email.map({True:"true",False:"false"})
df.to_csv(OUTPUT,index=False,encoding="utf-8")
print(f"Entrée={initial}; doublons exacts supprimés={removed}; sortie={len(df)}; lignes e-mail dupliqué={int(dupmask.sum())}")
print(f"CSV écrit: {OUTPUT}")
