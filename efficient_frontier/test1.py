import pandas as pd
from sklearn.covariance import EllipticEnvelope

outlier = EllipticEnvelope(contamination = 0.2)
data = pd.read_csv("results_frame_test.csv", index_col = 0)

outlier.fit(data)

prediction = outlier.predict(data)


