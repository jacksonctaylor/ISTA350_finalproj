import requests
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn.linear_model import LinearRegression


def scrape():
    url = "https://figshare.com/articles/dataset/Sample_details_and_ELISA_results_for_590_samples_/13362718?file=25751692"

    id = re.search(r'/(\d+)\?file=',url).group(1)


    api = "https://api.figshare.com/v2/articles/" + str(id)

    r = requests.get(api)
    data = r.json()

    download_url = data['files'][0]['download_url']

    df = pd.read_excel(download_url)

    return df
    #print(df.head())



def reg(df):
    biomarkers = ['LYVE1 ng/ml', 'REG1B ng/ml', 'TFF1 ng/ml', 'REG1A ng/ml']


    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for i, biomarker in enumerate(biomarkers):

        df_new = df[['Plasma CA19-9 U/ml',biomarker, 'Diagnosis (1=Control, 2=Benign, 3=PDAC)']].dropna()

        print(df_new)


        sns.scatterplot(
            data=df_new,
            x='Plasma CA19-9 U/ml',
            y=biomarker,
            hue='Diagnosis (1=Control, 2=Benign, 3=PDAC)',  
            ax=axes[i],
            legend = False
        )
    

        x = df_new['Plasma CA19-9 U/ml']
        y = df_new[biomarker]
        m, b = np.polyfit(x, y, 1)
    
        print(m)
        print(b)

        line_x = np.linspace(x.min(), x.max(), 100)
        line_y = m * line_x + b
        axes[i].plot(line_x, line_y, color='red', lw=2)  
   


        axes[i].set_title('CA19-9 vs. '+ str(biomarker).split()[0])
        axes[i].set_xlabel('Plasma CA19-9 U/ml')
        axes[i].set_ylabel(biomarker)



    plt.tight_layout()
    plt.show()

def log_of_1(df):
    biomarkers = ['LYVE1 ng/ml', 'REG1B ng/ml', 'TFF1 ng/ml', 'REG1A ng/ml']


    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for i, biomarker in enumerate(biomarkers):

        df_new = df[['Plasma CA19-9 U/ml',biomarker, 'Diagnosis (1=Control, 2=Benign, 3=PDAC)']].dropna()

        print(df_new)


        sns.scatterplot(
            data=df_new,
            x='Plasma CA19-9 U/ml',
            y=biomarker,
            hue='Diagnosis (1=Control, 2=Benign, 3=PDAC)',  
            ax=axes[i],
        )

        axes[i].legend(loc='upper left', title = 'Diagnosis (1=Control, 2=Benign, 3=PDAC)')
        axes[i].set_title('CA19-9 vs. '+ str(biomarker).split()[0])
        axes[i].set_xlabel('Plasma CA19-9 U/ml')
        axes[i].set_ylabel(biomarker)

        axes[i].set_xscale('log')
        axes[i].set_yscale('log')


    plt.tight_layout()
    plt.show()


def stage_n_CA19(df):
    pdac_df = df[df['Diagnosis (1=Control, 2=Benign, 3=PDAC)'] == 3].copy()


    pdac_df = pdac_df[['Plasma CA19-9 U/ml', 'Stage']].dropna()


    pdac_df['Stage'] = pdac_df['Stage'].replace(['IA','IB'],'I')
    pdac_df['Stage'] = pdac_df['Stage'].replace(['IIA','IIB'],'II')
    #print(pdac_df)



    plt.figure(figsize=(8, 6), facecolor='lightgray')
    sns.boxplot(data=pdac_df, x='Stage', y='Plasma CA19-9 U/ml', showfliers=False)
    sns.stripplot(data=pdac_df, x='Stage', y='Plasma CA19-9 U/ml', color='black', alpha=0.4)
    plt.xlabel('PDAC Stage')
    plt.ylabel('CA19-9 Concentration (U/ml)')
    plt.title('CA19-9 Levels by PDAC Progression', fontsize = 15)
    plt.yscale('log')
    counts = pdac_df['Stage'].value_counts()
    #print(counts)
    sorted_counts = counts.sort_index()
    #print(sorted_counts)
    for i, stage in enumerate(sorted_counts.index):
        n = sorted_counts[stage]
        plt.text(x=i, y=0.39, s= 'n = '+str(n), ha='center', fontsize=8)

    plt.show()

def heat(df):
    biomarkers = ['LYVE1 ng/ml', 'REG1B ng/ml', 'TFF1 ng/ml', 'REG1A ng/ml']


    di = []
    for i in df.index:
        if df.loc[i,'Diagnosis (1=Control, 2=Benign, 3=PDAC)'] == 3:
            di.append(df.loc[i,'Stage'])
        else:
            di.append(df.loc[i,'Diagnosis (1=Control, 2=Benign, 3=PDAC)'])
        
    for i, stage in enumerate(di):
        if stage == 'IA' or stage == 'IB':
            di[i] = 'I'
        if stage == 'IIA' or stage == 'IIB':
            di[i] = 'II'

    df['Diagnosis'] = di
    fix, axes = plt.subplots(1,2,figsize=(15,6))

    heatmap_data = df.dropna(subset=biomarkers + ['Diagnosis'])
    heatmap_dfmean = heatmap_data.groupby('Diagnosis')[biomarkers].mean()
    heatmap_dfmedian = heatmap_data.groupby('Diagnosis')[biomarkers].median()
    sns.heatmap(heatmap_dfmean, annot=True, cmap='coolwarm', ax=axes[0])
    sns.heatmap(heatmap_dfmedian, annot=True, cmap='coolwarm',ax=axes[1])
    axes[0].set_ylabel('Diagnosis (control = 1, benign = 2, PDAC I-IV)', fontsize = 7)
    axes[1].set_ylabel('Diagnosis (control = 1, benign = 2, PDAC I-IV)', fontsize = 7)
    axes[0].set_xlabel('Biomarkers', fontsize = 7)
    axes[1].set_xlabel('Biomarkers', fontsize = 7)
    axes[0].set_title('Mean Biomarker Expression by Diagnosis')
    axes[1].set_title('Median Biomarker Expression by Diagnosis')
    plt.show()


def main():
    '''
    '''
    df = scrape()
    #reg(df)
    #log_of_1(df)
    #stage_n_CA19(df)
    heat(df)

if __name__ == "__main__":
    main()

