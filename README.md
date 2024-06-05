The project is divided into 3 somewhat independent parts:
1. Crawler saves the HTML files with individual lots
2. export_to_S3 is a wrapper around Parcer that go through all html files and creates data.csv. For convenience, it's then pushed to S3
3. Collab notebook imports the data file from S3, explores the dataset, and provides the ML model for price prediction
