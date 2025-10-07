def model(dbt, session):
    dbt.config(submission_method="bigframes", timeout=6000)

    dataset = "bigquery-public-data.epa_historical_air_quality"
    index_columns = ["state_name", "county_name", "site_num", "date_local", "time_local"]
    param_column = "parameter_name"
    value_column = "sample_measurement"
    params_dfs = []

    table_param_dict = {
        "co_hourly_summary": "co",
        "no2_hourly_summary": "no2",
        "o3_hourly_summary": "o3",
        "pressure_hourly_summary": "pressure",
        "so2_hourly_summary": "so2",
        "temperature_hourly_summary": "temperature",
    }

    for table, param in table_param_dict.items():
        param_df = bpd.read_gbq(f"{dataset}.{table}", columns=index_columns + [value_column])
        param_df = param_df.sort_values(index_columns).drop_duplicates(index_columns).set_index(index_columns).rename(columns={value_column: param})
        params_dfs.append(param_df)

    wind_table = f"{dataset}.wind_hourly_summary"
    wind_speed_df = bpd.read_gbq(
        wind_table,
        columns=index_columns + [value_column],
        filters=[(param_column, "==", "Wind Speed - Resultant")]
    )
    wind_speed_df = wind_speed_df.sort_values(index_columns).drop_duplicates(index_columns).set_index(index_columns).rename(columns={value_column: "wind_speed"})
    params_dfs.append(wind_speed_df)

    df = bpd.concat(params_dfs, axis=1, join="inner")
    return df.reset_index()