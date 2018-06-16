
# PyCity Schools Analysis

* As a whole, schools with higher budgets, did not yield better test results. By contrast, schools with higher spending per student actually (\$645-675) underperformed compared to schools with smaller budgets (<\$585 per student).

* As a whole, smaller and medium sized schools dramatically out-performed large sized schools on passing math performances (89-91% passing vs 67%).

* As a whole, charter schools out-performed the public district schools across all metrics. However, more analysis will be required to glean if the effect is due to school practices or the fact that charter schools tend to serve smaller student populations per school. 
---


```python
import pandas as pd
file1 = 'raw_data/schools_complete.csv' 
file2 = 'raw_data/students_complete.csv'

df_school = pd.read_csv(file1)
df_student = pd.read_csv(file2)
```

## District Summary


```python
df_summary = pd.DataFrame(
    {
        'Total Schools':15,
        'Total Students': '{:,d}'.format(df_school['size'].sum()),
        'Total Budget': '${:,.2f}'.format(df_school['budget'].sum()),
        'Average Math Score': df_student['math_score'].mean(),
        'Average Reading Score': df_student['reading_score'].mean(),
        '% Passing Math': df_student.loc[df_student['math_score']>=71,:]['math_score'].count()/df_student['name'].count()*100,
        '% Passing Reading': df_student.loc[df_student['reading_score']>=71,:]['reading_score'].count()/df_student['name'].count()*100,
        '% Overall Passing Rate': (df_student.loc[df_student['math_score']>=71,:]['math_score'].count()/df_student['name'].count()+df_student.loc[df_student['reading_score']>=71,:]['reading_score'].count()/df_student['name'].count())/2*100
    }, index=[0]
)
df_summary
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>% Overall Passing Rate</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>Total Budget</th>
      <th>Total Schools</th>
      <th>Total Students</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>77.681899</td>
      <td>72.392137</td>
      <td>82.971662</td>
      <td>78.985371</td>
      <td>81.87784</td>
      <td>$24,649,428.00</td>
      <td>15</td>
      <td>39,170</td>
    </tr>
  </tbody>
</table>
</div>



## School Summary


```python
df_school_sum = df_school.rename(columns={'name':'school','type':'School Type','size':'Total Students','budget':'Total Budget'})
df_school_sum['Per Student Budget'] = df_school_sum['Total Budget'] / df_school_sum['Total Students']
```


```python
df_avgmath = pd.DataFrame(df_student.groupby(['school'])['math_score'].mean()).reset_index()
df_school_sum = pd.merge(df_avgmath, df_school_sum, on="school", how="right")
```


```python
df_school_sum = df_school_sum.rename(columns={'math_score':'Average Math Score'})
```


```python
df_avgread = pd.DataFrame(df_student.groupby(['school'])['reading_score'].mean()).reset_index()
df_school_sum = pd.merge(df_avgread, df_school_sum, on="school", how="right")
```


```python
df_school_sum = df_school_sum.rename(columns={'reading_score':'Average Reading Score'})
```


```python
df_math_70 = df_student[df_student['math_score']>70]
df_math_pass = df_math_70.groupby(['school'])['math_score'].count() / df_student.groupby(['school'])['math_score'].count()
df_math_pass = pd.DataFrame(df_math_pass).reset_index()
```


```python
df_school_sum = pd.merge(df_math_pass, df_school_sum, on="school", how="right")
```


```python
df_school_sum = df_school_sum.rename(columns={'math_score':'% Passing Math'})
```


```python
df_read_70 = df_student[df_student['reading_score']>70]
df_read_pass = df_read_70.groupby(['school'])['reading_score'].count() / df_student.groupby(['school'])['reading_score'].count()
df_read_pass = pd.DataFrame(df_read_pass).reset_index()
```


```python
df_school_sum = pd.merge(df_read_pass, df_school_sum, on="school", how="right")
df_school_sum = df_school_sum.rename(columns={'reading_score':'% Passing Reading'})
```


```python
df_school_sum['% Overall Passing Rate'] = (df_school_sum['% Passing Reading'] + df_school_sum['% Passing Math'])/2
```


```python
df_school_sum['% Passing Reading'] = df_school_sum['% Passing Reading'] * 100
df_school_sum['% Passing Math'] = df_school_sum['% Passing Math'] * 100
df_school_sum['% Overall Passing Rate'] = df_school_sum['% Overall Passing Rate'] * 100
```


```python
df_school_sum['Total Budget'] = df_school_sum['Total Budget'].map("${:.2f}".format)
df_school_sum['Per Student Budget'] = df_school_sum['Per Student Budget'].map("${:.2f}".format)
```


```python
df_school_sum
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
      <th>% Passing Reading</th>
      <th>% Passing Math</th>
      <th>Average Reading Score</th>
      <th>Average Math Score</th>
      <th>School ID</th>
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total Budget</th>
      <th>Per Student Budget</th>
      <th>% Overall Passing Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bailey High School</td>
      <td>79.300643</td>
      <td>64.630225</td>
      <td>81.033963</td>
      <td>77.048432</td>
      <td>7</td>
      <td>District</td>
      <td>4976</td>
      <td>$3124928.00</td>
      <td>$628.00</td>
      <td>71.965434</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cabrera High School</td>
      <td>93.864370</td>
      <td>89.558665</td>
      <td>83.975780</td>
      <td>83.061895</td>
      <td>6</td>
      <td>Charter</td>
      <td>1858</td>
      <td>$1081356.00</td>
      <td>$582.00</td>
      <td>91.711518</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Figueroa High School</td>
      <td>78.433367</td>
      <td>63.750424</td>
      <td>81.158020</td>
      <td>76.711767</td>
      <td>1</td>
      <td>District</td>
      <td>2949</td>
      <td>$1884411.00</td>
      <td>$639.00</td>
      <td>71.091896</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ford High School</td>
      <td>77.510040</td>
      <td>65.753925</td>
      <td>80.746258</td>
      <td>77.102592</td>
      <td>13</td>
      <td>District</td>
      <td>2739</td>
      <td>$1763916.00</td>
      <td>$644.00</td>
      <td>71.631982</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Griffin High School</td>
      <td>93.392371</td>
      <td>89.713896</td>
      <td>83.816757</td>
      <td>83.351499</td>
      <td>4</td>
      <td>Charter</td>
      <td>1468</td>
      <td>$917500.00</td>
      <td>$625.00</td>
      <td>91.553134</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Hernandez High School</td>
      <td>78.187702</td>
      <td>64.746494</td>
      <td>80.934412</td>
      <td>77.289752</td>
      <td>3</td>
      <td>District</td>
      <td>4635</td>
      <td>$3022020.00</td>
      <td>$652.00</td>
      <td>71.467098</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Holden High School</td>
      <td>92.740047</td>
      <td>90.632319</td>
      <td>83.814988</td>
      <td>83.803279</td>
      <td>8</td>
      <td>Charter</td>
      <td>427</td>
      <td>$248087.00</td>
      <td>$581.00</td>
      <td>91.686183</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Huang High School</td>
      <td>78.813850</td>
      <td>63.318478</td>
      <td>81.182722</td>
      <td>76.629414</td>
      <td>0</td>
      <td>District</td>
      <td>2917</td>
      <td>$1910635.00</td>
      <td>$655.00</td>
      <td>71.066164</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Johnson High School</td>
      <td>78.281874</td>
      <td>63.852132</td>
      <td>80.966394</td>
      <td>77.072464</td>
      <td>12</td>
      <td>District</td>
      <td>4761</td>
      <td>$3094650.00</td>
      <td>$650.00</td>
      <td>71.067003</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>92.203742</td>
      <td>91.683992</td>
      <td>84.044699</td>
      <td>83.839917</td>
      <td>9</td>
      <td>Charter</td>
      <td>962</td>
      <td>$585858.00</td>
      <td>$609.00</td>
      <td>91.943867</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Rodriguez High School</td>
      <td>77.744436</td>
      <td>64.066017</td>
      <td>80.744686</td>
      <td>76.842711</td>
      <td>11</td>
      <td>District</td>
      <td>3999</td>
      <td>$2547363.00</td>
      <td>$637.00</td>
      <td>70.905226</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Shelton High School</td>
      <td>92.617831</td>
      <td>89.892107</td>
      <td>83.725724</td>
      <td>83.359455</td>
      <td>2</td>
      <td>Charter</td>
      <td>1761</td>
      <td>$1056600.00</td>
      <td>$600.00</td>
      <td>91.254969</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Thomas High School</td>
      <td>92.905199</td>
      <td>90.214067</td>
      <td>83.848930</td>
      <td>83.418349</td>
      <td>14</td>
      <td>Charter</td>
      <td>1635</td>
      <td>$1043130.00</td>
      <td>$638.00</td>
      <td>91.559633</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Wilson High School</td>
      <td>93.254490</td>
      <td>90.932983</td>
      <td>83.989488</td>
      <td>83.274201</td>
      <td>5</td>
      <td>Charter</td>
      <td>2283</td>
      <td>$1319574.00</td>
      <td>$578.00</td>
      <td>92.093736</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Wright High School</td>
      <td>93.444444</td>
      <td>90.277778</td>
      <td>83.955000</td>
      <td>83.682222</td>
      <td>10</td>
      <td>Charter</td>
      <td>1800</td>
      <td>$1049400.00</td>
      <td>$583.00</td>
      <td>91.861111</td>
    </tr>
  </tbody>
</table>
</div>



## Top Performing Schools (By Passing Rate)


```python
df_school_sum.sort_values(['% Overall Passing Rate'], ascending=False).head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
      <th>% Passing Reading</th>
      <th>% Passing Math</th>
      <th>Average Reading Score</th>
      <th>Average Math Score</th>
      <th>School ID</th>
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total Budget</th>
      <th>Per Student Budget</th>
      <th>% Overall Passing Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>13</th>
      <td>Wilson High School</td>
      <td>93.254490</td>
      <td>90.932983</td>
      <td>83.989488</td>
      <td>83.274201</td>
      <td>5</td>
      <td>Charter</td>
      <td>2283</td>
      <td>$1319574.00</td>
      <td>$578.00</td>
      <td>92.093736</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>92.203742</td>
      <td>91.683992</td>
      <td>84.044699</td>
      <td>83.839917</td>
      <td>9</td>
      <td>Charter</td>
      <td>962</td>
      <td>$585858.00</td>
      <td>$609.00</td>
      <td>91.943867</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Wright High School</td>
      <td>93.444444</td>
      <td>90.277778</td>
      <td>83.955000</td>
      <td>83.682222</td>
      <td>10</td>
      <td>Charter</td>
      <td>1800</td>
      <td>$1049400.00</td>
      <td>$583.00</td>
      <td>91.861111</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cabrera High School</td>
      <td>93.864370</td>
      <td>89.558665</td>
      <td>83.975780</td>
      <td>83.061895</td>
      <td>6</td>
      <td>Charter</td>
      <td>1858</td>
      <td>$1081356.00</td>
      <td>$582.00</td>
      <td>91.711518</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Holden High School</td>
      <td>92.740047</td>
      <td>90.632319</td>
      <td>83.814988</td>
      <td>83.803279</td>
      <td>8</td>
      <td>Charter</td>
      <td>427</td>
      <td>$248087.00</td>
      <td>$581.00</td>
      <td>91.686183</td>
    </tr>
  </tbody>
</table>
</div>



## Bottom Performing Schools (By Passing Rate)


```python
df_school_sum.sort_values(['% Overall Passing Rate'], ascending=False).tail()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
      <th>% Passing Reading</th>
      <th>% Passing Math</th>
      <th>Average Reading Score</th>
      <th>Average Math Score</th>
      <th>School ID</th>
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total Budget</th>
      <th>Per Student Budget</th>
      <th>% Overall Passing Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>5</th>
      <td>Hernandez High School</td>
      <td>78.187702</td>
      <td>64.746494</td>
      <td>80.934412</td>
      <td>77.289752</td>
      <td>3</td>
      <td>District</td>
      <td>4635</td>
      <td>$3022020.00</td>
      <td>$652.00</td>
      <td>71.467098</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Figueroa High School</td>
      <td>78.433367</td>
      <td>63.750424</td>
      <td>81.158020</td>
      <td>76.711767</td>
      <td>1</td>
      <td>District</td>
      <td>2949</td>
      <td>$1884411.00</td>
      <td>$639.00</td>
      <td>71.091896</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Johnson High School</td>
      <td>78.281874</td>
      <td>63.852132</td>
      <td>80.966394</td>
      <td>77.072464</td>
      <td>12</td>
      <td>District</td>
      <td>4761</td>
      <td>$3094650.00</td>
      <td>$650.00</td>
      <td>71.067003</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Huang High School</td>
      <td>78.813850</td>
      <td>63.318478</td>
      <td>81.182722</td>
      <td>76.629414</td>
      <td>0</td>
      <td>District</td>
      <td>2917</td>
      <td>$1910635.00</td>
      <td>$655.00</td>
      <td>71.066164</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Rodriguez High School</td>
      <td>77.744436</td>
      <td>64.066017</td>
      <td>80.744686</td>
      <td>76.842711</td>
      <td>11</td>
      <td>District</td>
      <td>3999</td>
      <td>$2547363.00</td>
      <td>$637.00</td>
      <td>70.905226</td>
    </tr>
  </tbody>
</table>
</div>



## Math Scores by Grade


```python
df_mathgrade = df_student.groupby(['grade','school'])['math_score'].mean().unstack(level=0)
#df_mathgrade = df_mathgrade.reset_index()
df_mathgrade.columns.name = None
df_mathgrade = df_mathgrade.reset_index()
df_mathgrade
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
      <th>10th</th>
      <th>11th</th>
      <th>12th</th>
      <th>9th</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bailey High School</td>
      <td>76.996772</td>
      <td>77.515588</td>
      <td>76.492218</td>
      <td>77.083676</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cabrera High School</td>
      <td>83.154506</td>
      <td>82.765560</td>
      <td>83.277487</td>
      <td>83.094697</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Figueroa High School</td>
      <td>76.539974</td>
      <td>76.884344</td>
      <td>77.151369</td>
      <td>76.403037</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ford High School</td>
      <td>77.672316</td>
      <td>76.918058</td>
      <td>76.179963</td>
      <td>77.361345</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Griffin High School</td>
      <td>84.229064</td>
      <td>83.842105</td>
      <td>83.356164</td>
      <td>82.044010</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Hernandez High School</td>
      <td>77.337408</td>
      <td>77.136029</td>
      <td>77.186567</td>
      <td>77.438495</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Holden High School</td>
      <td>83.429825</td>
      <td>85.000000</td>
      <td>82.855422</td>
      <td>83.787402</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Huang High School</td>
      <td>75.908735</td>
      <td>76.446602</td>
      <td>77.225641</td>
      <td>77.027251</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Johnson High School</td>
      <td>76.691117</td>
      <td>77.491653</td>
      <td>76.863248</td>
      <td>77.187857</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>83.372000</td>
      <td>84.328125</td>
      <td>84.121547</td>
      <td>83.625455</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Rodriguez High School</td>
      <td>76.612500</td>
      <td>76.395626</td>
      <td>77.690748</td>
      <td>76.859966</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Shelton High School</td>
      <td>82.917411</td>
      <td>83.383495</td>
      <td>83.778976</td>
      <td>83.420755</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Thomas High School</td>
      <td>83.087886</td>
      <td>83.498795</td>
      <td>83.497041</td>
      <td>83.590022</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Wilson High School</td>
      <td>83.724422</td>
      <td>83.195326</td>
      <td>83.035794</td>
      <td>83.085578</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Wright High School</td>
      <td>84.010288</td>
      <td>83.836782</td>
      <td>83.644986</td>
      <td>83.264706</td>
    </tr>
  </tbody>
</table>
</div>



## Reading Score by Grade 


```python
df_readgrade = df_student.groupby(['grade','school'])['reading_score'].mean().unstack(level=0)
df_readgrade.columns.name = None
df_readgrade = df_readgrade.reset_index()
df_readgrade
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
      <th>10th</th>
      <th>11th</th>
      <th>12th</th>
      <th>9th</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bailey High School</td>
      <td>80.907183</td>
      <td>80.945643</td>
      <td>80.912451</td>
      <td>81.303155</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cabrera High School</td>
      <td>84.253219</td>
      <td>83.788382</td>
      <td>84.287958</td>
      <td>83.676136</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Figueroa High School</td>
      <td>81.408912</td>
      <td>80.640339</td>
      <td>81.384863</td>
      <td>81.198598</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ford High School</td>
      <td>81.262712</td>
      <td>80.403642</td>
      <td>80.662338</td>
      <td>80.632653</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Griffin High School</td>
      <td>83.706897</td>
      <td>84.288089</td>
      <td>84.013699</td>
      <td>83.369193</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Hernandez High School</td>
      <td>80.660147</td>
      <td>81.396140</td>
      <td>80.857143</td>
      <td>80.866860</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Holden High School</td>
      <td>83.324561</td>
      <td>83.815534</td>
      <td>84.698795</td>
      <td>83.677165</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Huang High School</td>
      <td>81.512386</td>
      <td>81.417476</td>
      <td>80.305983</td>
      <td>81.290284</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Johnson High School</td>
      <td>80.773431</td>
      <td>80.616027</td>
      <td>81.227564</td>
      <td>81.260714</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>83.612000</td>
      <td>84.335938</td>
      <td>84.591160</td>
      <td>83.807273</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Rodriguez High School</td>
      <td>80.629808</td>
      <td>80.864811</td>
      <td>80.376426</td>
      <td>80.993127</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Shelton High School</td>
      <td>83.441964</td>
      <td>84.373786</td>
      <td>82.781671</td>
      <td>84.122642</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Thomas High School</td>
      <td>84.254157</td>
      <td>83.585542</td>
      <td>83.831361</td>
      <td>83.728850</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Wilson High School</td>
      <td>84.021452</td>
      <td>83.764608</td>
      <td>84.317673</td>
      <td>83.939778</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Wright High School</td>
      <td>83.812757</td>
      <td>84.156322</td>
      <td>84.073171</td>
      <td>83.833333</td>
    </tr>
  </tbody>
</table>
</div>



## Scores by School Spending


```python
bins = [0,585,615,645,675]
labels = ['<$585','$585-615','$615-645','$645-675']
```


```python
df_spending = df_school_sum[['school','Average Math Score','Average Reading Score','% Passing Math','% Passing Reading','% Overall Passing Rate','Per Student Budget']]
```


```python
df_spending['Per Student Budget'] = df_spending["Per Student Budget"].str.replace('$','')
df_spending['Per Student Budget'] = pd.to_numeric(df_spending['Per Student Budget'])
df_spending
```

    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:1: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      """Entry point for launching an IPython kernel.
    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:2: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>school</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
      <th>Per Student Budget</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Bailey High School</td>
      <td>77.048432</td>
      <td>81.033963</td>
      <td>64.630225</td>
      <td>79.300643</td>
      <td>71.965434</td>
      <td>628.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Cabrera High School</td>
      <td>83.061895</td>
      <td>83.975780</td>
      <td>89.558665</td>
      <td>93.864370</td>
      <td>91.711518</td>
      <td>582.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Figueroa High School</td>
      <td>76.711767</td>
      <td>81.158020</td>
      <td>63.750424</td>
      <td>78.433367</td>
      <td>71.091896</td>
      <td>639.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Ford High School</td>
      <td>77.102592</td>
      <td>80.746258</td>
      <td>65.753925</td>
      <td>77.510040</td>
      <td>71.631982</td>
      <td>644.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Griffin High School</td>
      <td>83.351499</td>
      <td>83.816757</td>
      <td>89.713896</td>
      <td>93.392371</td>
      <td>91.553134</td>
      <td>625.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Hernandez High School</td>
      <td>77.289752</td>
      <td>80.934412</td>
      <td>64.746494</td>
      <td>78.187702</td>
      <td>71.467098</td>
      <td>652.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Holden High School</td>
      <td>83.803279</td>
      <td>83.814988</td>
      <td>90.632319</td>
      <td>92.740047</td>
      <td>91.686183</td>
      <td>581.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Huang High School</td>
      <td>76.629414</td>
      <td>81.182722</td>
      <td>63.318478</td>
      <td>78.813850</td>
      <td>71.066164</td>
      <td>655.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Johnson High School</td>
      <td>77.072464</td>
      <td>80.966394</td>
      <td>63.852132</td>
      <td>78.281874</td>
      <td>71.067003</td>
      <td>650.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Pena High School</td>
      <td>83.839917</td>
      <td>84.044699</td>
      <td>91.683992</td>
      <td>92.203742</td>
      <td>91.943867</td>
      <td>609.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Rodriguez High School</td>
      <td>76.842711</td>
      <td>80.744686</td>
      <td>64.066017</td>
      <td>77.744436</td>
      <td>70.905226</td>
      <td>637.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Shelton High School</td>
      <td>83.359455</td>
      <td>83.725724</td>
      <td>89.892107</td>
      <td>92.617831</td>
      <td>91.254969</td>
      <td>600.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Thomas High School</td>
      <td>83.418349</td>
      <td>83.848930</td>
      <td>90.214067</td>
      <td>92.905199</td>
      <td>91.559633</td>
      <td>638.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Wilson High School</td>
      <td>83.274201</td>
      <td>83.989488</td>
      <td>90.932983</td>
      <td>93.254490</td>
      <td>92.093736</td>
      <td>578.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Wright High School</td>
      <td>83.682222</td>
      <td>83.955000</td>
      <td>90.277778</td>
      <td>93.444444</td>
      <td>91.861111</td>
      <td>583.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_spending["Range"] = pd.cut(df_spending["Per Student Budget"], bins, labels=labels)
```

    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:1: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      """Entry point for launching an IPython kernel.
    


```python
df_spending = df_spending.groupby(['Range']).mean()
```


```python
del df_spending['Per Student Budget']
```


```python
df_spending
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>Range</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;$585</th>
      <td>83.455399</td>
      <td>83.933814</td>
      <td>90.350436</td>
      <td>93.325838</td>
      <td>91.838137</td>
    </tr>
    <tr>
      <th>$585-615</th>
      <td>83.599686</td>
      <td>83.885211</td>
      <td>90.788049</td>
      <td>92.410786</td>
      <td>91.599418</td>
    </tr>
    <tr>
      <th>$615-645</th>
      <td>79.079225</td>
      <td>81.891436</td>
      <td>73.021426</td>
      <td>83.214343</td>
      <td>78.117884</td>
    </tr>
    <tr>
      <th>$645-675</th>
      <td>76.997210</td>
      <td>81.027843</td>
      <td>63.972368</td>
      <td>78.427809</td>
      <td>71.200088</td>
    </tr>
  </tbody>
</table>
</div>



## Scores by School Size


```python
bins = [0,1000,2000,5000]
labels = ['Small (<1000)','Medium (1000-2000)','Large (2000-5000)']
```


```python
df_size = df_school_sum[['school','Average Math Score','Average Reading Score','% Passing Math','% Passing Reading','% Overall Passing Rate','Total Students']]
```


```python
df_size["Range"] = pd.cut(df_size['Total Students'], bins, labels=labels)
```

    C:\ProgramData\Anaconda3\lib\site-packages\ipykernel_launcher.py:1: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: http://pandas.pydata.org/pandas-docs/stable/indexing.html#indexing-view-versus-copy
      """Entry point for launching an IPython kernel.
    


```python
df_size = df_size.groupby(['Range']).mean()
df_size
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
      <th>Total Students</th>
    </tr>
    <tr>
      <th>Range</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Small (&lt;1000)</th>
      <td>83.821598</td>
      <td>83.929843</td>
      <td>91.158155</td>
      <td>92.471895</td>
      <td>91.815025</td>
      <td>694.500</td>
    </tr>
    <tr>
      <th>Medium (1000-2000)</th>
      <td>83.374684</td>
      <td>83.864438</td>
      <td>89.931303</td>
      <td>93.244843</td>
      <td>91.588073</td>
      <td>1704.400</td>
    </tr>
    <tr>
      <th>Large (2000-5000)</th>
      <td>77.746417</td>
      <td>81.344493</td>
      <td>67.631335</td>
      <td>80.190800</td>
      <td>73.911067</td>
      <td>3657.375</td>
    </tr>
  </tbody>
</table>
</div>



## Scores by School Type


```python
df_type = df_school_sum.groupby('School Type').mean()
```


```python
df_type = df_type[['Average Math Score','Average Reading Score','% Passing Math','% Passing Reading','% Overall Passing Rate']]
```


```python
df_type
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School Type</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Charter</th>
      <td>83.473852</td>
      <td>83.896421</td>
      <td>90.363226</td>
      <td>93.052812</td>
      <td>91.708019</td>
    </tr>
    <tr>
      <th>District</th>
      <td>76.956733</td>
      <td>80.966636</td>
      <td>64.302528</td>
      <td>78.324559</td>
      <td>71.313543</td>
    </tr>
  </tbody>
</table>
</div>


