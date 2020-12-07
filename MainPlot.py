class Genie:
    def predict_ml(self, df):
        df = df.iloc[::-1] # reverse data-frame
        df = df[['Close']]
        future_days = 30 # variable to predict 'x' days
        df['Prediction'] = df[['Close']].shift(-future_days)

        #creating a feature data set converted to numpy array without the last 'x' rows
        x = np.array(df.drop(['Prediction'], 1))[:-future_days]
        y = np.array(df['Prediction'])[:-future_days]
        #Split the data for training and testing
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.1)
        tree = DecisionTreeRegressor().fit(x_train, y_train)

        #Get the last 'x' rows from the feature data set
        x_future = df.drop(['Prediction'], 1)[:-future_days]
        x_future = x_future.tail(future_days)
        x_future = np.array(x_future)
        #Show the model tree prediction
        tree_prediction = tree.predict(x_future)
        test = pd.DataFrame()
        test['Tree'] = tree_prediction
        #Create a current range
        start = datetime.date.today()
        date_generated = [start + datetime.timedelta(days=x) for x in range(future_days)]
        date_table = []
        for date in date_generated:
            date_table.append(date.strftime("%Y-%m-%d"))
        test['Date'] = date_table
        print(test)
        #Visualizing the data
        fig_p = px.line(test, x = 'Date', y = 'Tree') #x:date; y:price
        fig_p.show()