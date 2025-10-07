def model(dbt, session):
    dbt.config(submission_method="bigframes", notebook_template_id="8573503490234515456")

    @bpd.udf(dataset='jialuo_test_us', name='jl_test')
    def my_func(x: int) -> int:
        return x * 1100

    data = {"int": [1, 2], "str": ['a', 'b']}
    bdf = bpd.DataFrame(data=data)
    bdf['int'] = bdf['int'].apply(my_func)

    return bdf


# def model(dbt, session):
#     dbt.config(submission_method="bigframes")

#     data = {"int": [1, 2, 3], "str": ['a', 'b165+mark', 'c']}
#     return bpd.DataFrame(data=data)