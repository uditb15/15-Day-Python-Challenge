## You are a Product Insights Analyst working with the Ben & Jerry's sales strategy team to investigate seasonal sales patterns through comprehensive data analysis. The team wants to understand how temperature variations and unique transaction characteristics impact ice cream sales volume. Your goal is to perform detailed data cleaning and exploratory analysis to uncover meaningful insights about seasonal sales performance.

### Question 1

Identify and remove any duplicate sales transactions from the dataset to ensure accurate analysis of seasonal patterns.

### Question 2

Create a pivot table to summarize the total sales volume of ice cream products by month and temperature range.
Use the following temperature bins where each bin includes the upper bound but not the lower:

- Less than 60 degrees
- 60 to less than 70 degrees
- 70 to less than 80 degrees
- 80 to less than 90 degrees
- 90 to less than 100 degrees
- 100 degrees or more

### Question 3

Can you detect any outliers in the monthly sales volume using the Inter Quartile Range (IQR) method? A month is considered an outlier if it falls below Q1 minus 1.5 times the IQR or above Q3 plus 1.5 times the IQR
