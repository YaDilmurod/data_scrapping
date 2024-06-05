from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import joblib
import pandas as pd

df = pd.read_excel('Data Scrapping/Data/Cleaned_Combined.xlsx')

columns_to_scale = ['num_of_rooms', 'area']
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(df[columns_to_scale])
X_scaled_df = pd.DataFrame(X_scaled, columns=columns_to_scale)
df = pd.concat([X_scaled_df, df.drop(columns_to_scale, axis=1)], axis=1)

joblib.dump(scaler, 'Data Scrapping/Code/Model/min_max_scaller.pkl')

X = df.drop(['source','price'], axis=1)
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=40)

model = GradientBoostingRegressor(
    learning_rate=0.01,
    n_estimators=300,
    max_depth=5,
    min_samples_split=10,
    min_samples_leaf=4,
    subsample=0.5
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

joblib.dump(model, 'Data Scrapping/Code/Model/GradientBoosting.pkl')
