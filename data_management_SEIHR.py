#!/usr/bin/env python
# coding: utf-8

# In[18]:


# ouvrir les packages
import plotly.graph_objects as go 
import pandas as pd
import numpy as np
import ssl
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.integrate import odeint

ssl._create_default_https_context = ssl._create_unverified_context


# In[216]:


# ouvrir le fichier des données

df = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7', sep=';')
#df = pd.read_csv('donnees-hospitalieres-covid19-2020-08-05-19h00.csv', sep=';')
df.head(10)


# In[217]:


df = df.dropna()


# ### Nettoyage des données

# In[218]:


df.index = df['jour'] # mettre en index les jours des pays
df = df.drop(['jour'], axis=1) # enlever la colonne jour dupliqué
df.head(10)


# In[219]:


df_described = df.describe()
df_described.head(20)


# In[21]:


df_dep_filtered = df.filter(['dep','jour','hosp','rea','rad','dc'])
df_dep_filtered.head(10)


# In[23]:


df_dep = df_dep_filtered.groupby('dep').sum()
df_dep.head(10)


# In[24]:


# Classer les departement par ordre de decroissance pour voir les departement les plus affecté 
df_sorted_by_dep = df_dep.sort_values(['dc','rea','rad','hosp'], ascending=False) 
df_sorted_by_dep.head(10)


# In[223]:


# Pie chart
fig = px.pie(df, values='dc', names='dep', title='Nombre de décès par département')
fig.show()


# In[154]:


fig = px.line(df, x=df.index, y='hosp', color='dep')
fig.show()


# In[221]:


# fonction afficher une courbe par département 
def trace_by_dep (criteria,first_name, second_dep) : 
        
        dep1 = df.loc[df['dep'] == first_name] 
        dep2 = df.loc[df['dep'] == second_dep] 
        plt.figure(figsize=(20,10))
        fig1 = plt.plot(dep1.index, dep1[criteria], label='Alpes Maritimes')
        fig2 = plt.plot(dep2.index, dep2[criteria], label='Hautes Alpes')
        plt.legend()
        plt.show()

        return fig1, fig2 
    
trace_by_dep ('hosp','06','05')

#dep


# ### Modélisation SEIHR 

# In[222]:


#Modélisation SIR 

def deriv(y, t, N,beta,alpha,lamb,gamma,mu):
    """
    y : liste contenant les 3 fonctions inconnus 
    t : le temps 
    beta, gamma : les deux facteurs du modèle
    """
    S,E,I,H,R = y 

  # Description des 3 equations differentielles 
    #dSdt = -S * I  * beta 
    #dIdt = S * I  * beta  - gamma * I 
    #dRdt = gamma * I 
    dSdt = - S * E* beta  
    dEdt =   beta * S * I -alpha*E -lamb*E 
    dIdt =   alpha* E -gamma*I 
    dHdt =   lamb*E + gamma*I 
    dRdt =   mu * I
    
    return dSdt, dEdt, dIdt, dHdt, dRdt 


# Au temps t0,  50% sains, 30% Exposé, 20% infecté, 0% Morts
y0 = 0.5, 0.3, 0.2, 0, 0 
t = np.linspace(0, 30)

# Paramètres du modèle 
v = 0.03      # taux de natalité en france
N = 67000000  # population initiale 46601
beta = 3.5    # taux de transmission 
alpha = 0.7   # taux d'incubation 
lamb = 0.6    # taux de guérison 
gamma =  0.7  # taux de gérison réel 
mu = 1.8      # taux de mortalité
epsilon = 0.035 # taux de rechute 


# Resolution des équations differentielles 
ret = odeint(deriv, y0, t, args = (N,beta,alpha,lamb,gamma,mu))
S,E,I,H,R = ret.T

plt.figure(figsize=(20,10))
plt.plot(t, S, label="Sains")
plt.plot(t, E,label="Exposés")
plt.plot(t, I, label="Inféctés")
plt.plot(t, H,label="Guéris")
plt.plot(t, R, label="Morts")

plt.xlabel("temps")
plt.ylabel("nombre d'individu")
plt.legend()
plt.title(f"Modélisation de la pandémie du COVID19 par un modèle SEIHR")


# ### Visualisation de l'impact des mesures sanitaires sur la pandémie
# 

# In[127]:


# séparer la BDD en deux dataset pendant et après confinement)
durant_conf = df.loc['2020-03-18':'2020-05-11']
apres_conf = df.loc['2020-05-12':'2020-08-31']


# In[129]:


durant_conf.head(10)
apres_conf.head(10)


# In[140]:


# Nombre d'hospitalisation pendant et apres le confinement
plt.figure(figsize=(20,10))
fig1 = plt.plot(durant_conf.index, durant_conf['hosp'], label="Nb hospitalisation pendant confinement")
fig2 = plt.plot(apres_conf.index, apres_conf['hosp'],   label="Nb hospitalisation après confinement")
plt.legend()
plt.show()


# In[141]:


# Nombre d'hospitalisation pendant et apres le confinement
plt.figure(figsize=(20,10))
fig1 = plt.plot(durant_conf.index, durant_conf['rea'], label="Nb de personnes en réanimation pendant confinement")
fig2 = plt.plot(apres_conf.index, apres_conf['rea'],   label="Nb de personnes en réanimation après confinement")
plt.legend()
plt.show()


# In[142]:


# Nombre d'hospitalisation pendant et apres le confinement
plt.figure(figsize=(20,10))
fig1 = plt.plot(durant_conf.index, durant_conf['rad'], label="Nb de personnes guéris pendant confinement")
fig2 = plt.plot(apres_conf.index, apres_conf['rad'],   label="Nb de personnes guéris après confinement")
plt.legend()
plt.show()


# In[143]:


# Nombre d'hospitalisation pendant et apres le confinement
plt.figure(figsize=(20,10))
fig1 = plt.plot(durant_conf.index, durant_conf['dc'], label="Nb de décès pendant confinement")
fig2 = plt.plot(apres_conf.index, apres_conf['dc'],   label="Nb de décès après confinement")
plt.legend()
plt.show()


# ### Comparaison du nombre de décès avec les données mondiale de Google

# In[169]:


# Les données seront consatemment mises à jour
df_RS = pd.read_csv('https://raw.githubusercontent.com/google-research/open-covid-19-data/master/data/exports/cc_by/aggregated_cc_by.csv', sep=',', low_memory=False)
#df_RS = pd.read_csv('https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv', sep=',',low_memory=False)
df_RS.head(10)


# In[170]:


# On récupère les données qui concerne la France
FR_df = df_RS[df_RS['region_code'] == 'FRA']
FR_df


# In[174]:


# On filtre les données
sub_FR_df = FR_df.filter(['deaths_cumulative','date'])
# mettre en indexe la date 
sub_FR_df.index = sub_FR_df['date'] 
sub_FR_df = sub_FR_df.drop(['date'], axis=1)
print(sub_FR_df)


# In[177]:


Google_df = sub_FR_df.loc['2020-03-18':'2020-08-31']
Google_df.head(10)


# In[188]:


# récupérér les données du début du confinement jusqu'à aujourd'hui et calculé leur somme cumulé
SPF_df = df.loc['2020-03-18':'2020-08-31']['dc'].cumsum()
SPF_df


# In[196]:


# Afficher le la somme cumulée des décès par Google
plt.figure(figsize=(15,10))
fig = plt.plot(Google_df.index, Google_df['deaths_cumulative'], label='Google Covid DB')
plt.legend()
plt.show()


# In[194]:


# Afficher le la somme cumulée des décès par Santé publique France
plt.figure(figsize=(15,10))
plt.plot(SPF_df, label='Santé Publique France')
plt.legend()
plt.show()

