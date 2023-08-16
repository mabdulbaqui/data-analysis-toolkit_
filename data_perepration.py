from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder


# def apply_pca_on_numerical(df, n_components=.95):
#     try:
#         # Separate numerical columns
#         numerical_features = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
#
#         # Check if there are any null values in the numerical columns
#         if df[numerical_features].isnull().values.any():
#             print("Warning: Null values found in the numerical columns. Fill or drop them before applying PCA.")
#
#         # Check if all numerical columns have the same length
#         if len(set(df[numerical_features].apply(len))) > 1:
#             print("Error: Numerical columns must have the same length for PCA.")
#
#         # Create a StandardScaler object for numerical data
#         scaler = StandardScaler()
#         df[numerical_features] = scaler.fit_transform(df[numerical_features])
#
#         # Apply PCA on numerical data
#         pca = PCA(n_components=n_components)
#         df[numerical_features] = pca.fit_transform(df[numerical_features])
#     except Exception as e:
#         print("Error occurred while applying PCA on numerical features.")
#         print(f"Error message: {str(e)}")

