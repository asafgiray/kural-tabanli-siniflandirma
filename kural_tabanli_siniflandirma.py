import pandas as pd

#Görüntü Ayarları
pd.set_option('display.max_rows', None)

#persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
df = pd.read_csv("persona.csv")
df.info()
df.shape
df.head()
df.tail()
df.describe().T

#Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].unique()
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

#Kaç unique PRICE vardır?
df["PRICE"].unique()
df["PRICE"].nunique()

#Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

#Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()
df.groupby("COUNTRY")["PRICE"].count()

#Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY").agg({"PRICE":"sum"})
df.groupby("COUNTRY")["PRICE"].sum()

#SOURCE türlerine göre satış sayıları nedir?
df["SOURCE"].value_counts()

#Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY").agg({"PRICE":"mean"})
df.groupby("COUNTRY")["PRICE"].mean()

#SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE":"mean"})
df.groupby("SOURCE")["PRICE"].mean()

#COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE":"mean"})
df.groupby(["COUNTRY","SOURCE"])["PRICE"].mean()

#COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"}).head()
df.groupby(["COUNTRY","SOURCE","SEX","AGE"])["PRICE"].mean()

#Çıktıyı PRICE’a göre sıralayınız.
agg_df = df.groupby(["COUNTRY","SOURCE","SEX","AGE"]).agg({"PRICE":"mean"}).sort_values("PRICE",ascending=False)
agg_df.head()

#Indekste yer alan isimleri değişken ismine çeviriniz.
agg_df = agg_df.reset_index()
agg_df.head()

#Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.
agg_df["AGE"].describe() #çeyreklikleri öğrendik

araliklar = [0,18,23,30,40,agg_df["AGE"].max()]
etiketler = ["0-18","19-23","24-30","31-40","41-"+str(agg_df["AGE"].max())]

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"],bins=araliklar,labels=etiketler) #age değerini bölme işlemi
agg_df.head()

#Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
agg_df.columns

for row in agg_df.values:
    print(row) #gözlem değerlerine ulaştık

[row[0].upper()+"_"+row[1].upper()+"_"+row[2].upper()+"_"+row[5].upper() for row in agg_df.values] #gerekli olan değerleri aldık

agg_df["CUSTOMERS_LEVEL_BASED"] = [row[0].upper()+"_"+row[1].upper()+"_"+row[2].upper()+"_"+row[5].upper() for row in agg_df.values] #veri tabanına ekledik

agg_df = agg_df[["CUSTOMERS_LEVEL_BASED","PRICE"]] #gereksiz değişkenleri çıkarttık, iki sütun kaldı
agg_df.head()

for i in agg_df["CUSTOMERS_LEVEL_BASED"].values:
    print(i.split("_")) #ayırma işlemi yaptık

agg_df = agg_df.groupby("CUSTOMERS_LEVEL_BASED").agg({"PRICE":"mean"}) #bu işlemin sebebi customers_leveldeki aynı olan değerleri ayıklayıp, teke düşürüp, o tek değere ortalama price değerini verme
agg_df = agg_df.reset_index()
agg_df.head()

agg_df["CUSTOMERS_LEVEL_BASED"].value_counts()
agg_df.head()

#Yeni müşterileri segmentlere ayırmak(Price segment)
agg_df["SEGMENT"] = pd.cut(agg_df["PRICE"],bins=4,labels=["D","C","B","A"]) #segmenti çeyreklikleri bölü labellarla adlandırdık
agg_df.head(30)
agg_df.groupby("SEGMENT").agg({"PRICE":"mean"}) #segmentlerin ortalama price değerine baktık

#Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
new_user="TUR_ANDROID_FEMALE_31-40"
agg_df[agg_df["CUSTOMERS_LEVEL_BASED"]==new_user]

new_user="FRA_IOS_MALE_19-23"
agg_df[agg_df["CUSTOMERS_LEVEL_BASED"]==new_user]
