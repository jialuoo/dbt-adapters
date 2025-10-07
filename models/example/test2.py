def model(dbt, session):
    dbt.config(
        submission_method="bigframes",
        packages=["scikit-learn ~=1.6.0", "mlflow==2.21.2", "numpy >= 2.1.0", "pandas", "flask == 3.1.0", "boto3<1.30.0"],
        # packages=['numpy>=2.1.1', 'pandas', 'mlflow'],
    )

    data = {'id': [0, 1, 2],'name': ['Brian', 'Isaac', 'Marie']}
    bdf = bpd.DataFrame(data)

    import mlflow, boto3
    print('mlflow version: ', mlflow.__version__)
    print('boto3 version: ', boto3.__version__)

    return bdf