def model(dbt, session):
    dbt.config(submission_method="bigframes", timeout=6000)

    df = dbt.ref("prepare_table")

    train_data_filter = (df.date_local.dt.year < 2017)
    test_data_filter = (df.date_local.dt.year >= 2017) & (df.date_local.dt.year < 2020)
    predict_data_filter = (df.date_local.dt.year >= 2020)

    index_columns = ["state_name", "county_name", "site_num", "date_local", "time_local"]
    df_train = df[train_data_filter].set_index(index_columns)
    df_test = df[test_data_filter].set_index(index_columns)
    df_predict = df[predict_data_filter].set_index(index_columns)

    X_train, y_train = df_train.drop(columns="o3"), df_train["o3"]
    X_test, y_test = df_test.drop(columns="o3"), df_test["o3"]
    X_predict = df_predict.drop(columns="o3")

    from bigframes.ml.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(X_train, y_train)
    df_pred = model.predict(X_predict)

    return df_pred