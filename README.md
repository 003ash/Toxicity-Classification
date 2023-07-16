# Toxicity-Classification

### Description:
This project aims to detect and classify hate speech into six categories: obscene, threatening, insulting, toxic, severely toxic, and identity hate. It utilizes machine learning models such as SVM, logistic regression, extra trees, XGBoost, and LSTM. The project addresses the challenges of multiclass and multilabel classification and incorporates classifier chains to improve performance. <br>
Out of the models mentioned, **XGBoost** preforms the best. 

## Output:
Model | Mean AUC_ROC score 
:---: | :---: 
SVM (Binary Relevance) | `0.66`
SVM (Classifier Chains) | `0.67`
Logistic Regression (Binary Relevance) | `0.73`
Logistic Regression (Classifier Chains) | `0.76`
Extra Trees | `0.93`
XGBoost | `0.96`

### Dataset and other files: 
https://drive.google.com/drive/folders/1kooEeZ5QE3eteVic6QINXOakli5VIBYZ?usp=sharing

### UI:

Home Screen:
![image](https://github.com/003ash/Toxicity-Classification/assets/64546134/38443b45-fc01-448c-a39d-c91af9137d85)

Output screen using the example "damn you idiot!":
![image](https://github.com/003ash/Toxicity-Classification/assets/64546134/5eae4af8-3b44-4473-8b10-022632941093)

