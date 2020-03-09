from pandas import DataFrame, concat

myDic1=DataFrame(data={'name':'abc', 'id':'def', 'parents':'hij'}, index=[0])
myDic2=DataFrame(data={'name':'123', 'id':'456', 'parents':'789'}, index=[0])

myDF1=DataFrame(myDic1)
myDF2=DataFrame(myDic2)

print(myDF1)
print(myDF2)

myDF3=concat([myDF1, myDF2], ignore_index=True)

print(myDF3)


